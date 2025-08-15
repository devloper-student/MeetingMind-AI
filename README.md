# MeetingMind-AI

## Project Overview

MeetingMind-AI is a cutting-edge AI-powered system designed to automate capturing, summarizing, and communicating business meeting insights with efficiency and professionalism. From raw audio recordings, the system delivers accurate transcriptions, extracts critical meeting highlights, sentiments, and action items, then seamlessly communicates outcomes via email.

---

## Key Features

- **Automated Audio Transcription:** Converts meeting audio files into accurate text using advanced speech recognition models like Mistral AI.
- **AI-Powered Summarization:** Distills lengthy discussions into concise, actionable meeting minutes including key financial highlights and growth strategies.
- **Sentiment Analysis:** Evaluates tone and sentiment to provide context to meeting outcomes.
- **Persistent Knowledge Output:** Generates detailed markdown files documenting summaries, action points, and sentiments.
- **Direct Gmail Integration:** Automatically sends professional emails with meeting minutes to stakeholders.
- **Robust Error Handling:** Handles API limits and encoding issues gracefully.

---

## Technology Stack

- Python 3.8+
- CrewAI Framework
- Mistral AI (Speech-to-Text; Language Models)
- Gmail API
- Pydantic (Data Validation and Schemas)
- Pydub (Audio Processing)

---

## Getting Started

### Prerequisites

- Python 3.8+ installed
- Mistral AI API key
- Google API credentials for Gmail access

### Installation

```bash
git clone https://github.com/devloper-student/MeetingMind-AI.git
cd MeetingMind-AI
pip install -r requirements.txt
```

### Configuration

Create a `.env` file and add the following:

```
MISTRAL_API_KEY=your_mistral_api_key_here
```

Place your meeting audio file as `EarningsCall.wav` in the project root directory.

### Usage

Run the main program:

```bash
python src/main.py
```

The system will generate transcripts, create summaries, write markdown meeting minutes files, and send emails to your configured recipients.

---

## System Architecture

```
Audio Input 1 Transcription 1 AI Analysis 1 Document Generation 1 Email Delivery
     1              1             1              1                1
  Pydub         Mistral AI    CrewAI Agents   File Output      Gmail API
```

---

## Demo

### Sample Output

- **Input**: `EarningsCall.wav` (30-minute meeting recording)
- **Generated Files**:
  - `meeting_minutes/summary.txt`
  - `meeting_minutes/action_items.txt` 
  - `meeting_minutes/sentiment.txt`
- **Email**: Professional meeting minutes sent to stakeholders

### Performance

- Transcription: ~2x audio length processing time
- Summarization: <30 seconds for typical meeting
- Email delivery: Real-time

---

## Contributing

Contributions, bug reports, and feature requests are warmly welcome! Feel free to open issues or submit pull requests.

---

## License

This project is licensed under the MIT License.
