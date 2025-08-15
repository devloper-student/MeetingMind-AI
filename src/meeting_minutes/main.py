#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from crews.meeting_minutes_crew.meeting_minutes_crew import MeetingMinutesCrew

from crews.gmailcrew.gmailcrew import Gmailcrew

# from meeting_minutes.crews.poem_crew.poem_crew import PoemCrew

from dotenv import load_dotenv

from pydub import AudioSegment

from pydub.utils import make_chunks

from pathlib import Path

import os
from mistralai import Mistral

load_dotenv()


class Meeting_minutesState(BaseModel):
    transcript: str = ""
    Meeting_minutes: str = ""


class Meeting_minutesFlow(Flow[Meeting_minutesState]):

    @start()
    def transcribe_meeting(self):
        print("Generating Transcription")

        # Retrieve the API key from environment variables
        api_key = os.environ["MISTRAL_API_KEY"]

        # Specify model
        model = "voxtral-mini-latest"

        # Initialize the Mistral client
        client = Mistral(api_key=api_key)

        SCRIPT_DIR = Path(__file__).parent

        audio = AudioSegment.from_wav(SCRIPT_DIR / "EarningsCall.wav")

        chunk_length_ms = 30000  # 30 seconds
        chunks = make_chunks(audio, chunk_length_ms)

        full_transcript = ""

        for i, chunk in enumerate(chunks):
            print(f"Processing and Transcribing chunk {i + 1}/{len(chunks)}")
            chunk_path = SCRIPT_DIR / f"chunk_{i}.wav"
            chunk.export(chunk_path, format="wav")
            with open(chunk_path, "rb") as f:
                transcription_response = client.audio.transcriptions.complete(
                    model=model,
                    file={
                        "content": f,
                        "file_name": "EarningsCall.wav",
                    },
                    # language="en"
                )
                full_transcript += transcription_response.text + " "

            os.remove(chunk_path)  # Clean up the chunk file

        # Print the content of the response
        print(full_transcript)

        self.state.transcript = full_transcript.strip()
        return self.state

    @listen(transcribe_meeting)
    def generate_meeting_minutes(self):
        print("Generating meeting minutes...")
        print(f"Transcript Length: {len(self.state.transcript)}")

        meeting_dir = Path("meeting_minutes")
        meeting_dir.mkdir(exist_ok=True)

        crew = MeetingMinutesCrew()

        inputs = {
            "transcript": self.state.transcript
        }
        Meeting_minutes = crew.crew().kickoff(inputs=inputs)
        self.state.Meeting_minutes = str(Meeting_minutes)
        return self.state

    @listen(generate_meeting_minutes)
    def draft_meeting_minutes(self):
        print("Drafting meeting minutes...")

        crew = Gmailcrew()

        inputs = {
            "body": self.state.Meeting_minutes
        }

        draft_crew = crew.crew().kickoff(inputs=inputs)
        print(draft_crew)

        return self.state


def kickoff():
    meeting_minutes_flow = Meeting_minutesFlow()
    meeting_minutes_flow.kickoff()


def plot():
    meeting_minutes_flow = Meeting_minutesFlow()
    meeting_minutes_flow.plot()


if __name__ == "__main__":
    kickoff()
