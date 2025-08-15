from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from . import gmail_utility_tool

authenticate_gmail = gmail_utility_tool.authenticate_gmail
create_message = gmail_utility_tool.create_message
create_draft = gmail_utility_tool.create_draft


class GmailInputTool(BaseModel):
    """Input schema for MyCustomTool."""

    body: str = Field(..., description="The email body to send.")


class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = GmailInputTool

    def _run(self, body: str) -> str:
        try:
            service = authenticate_gmail()

            sender = "Sender Name <sender_email@gmail.com>"
            to = "Recipient Name <recipient_email@gmail.com>"
            subject = "Meeting_minutes"
            message_txt = body

            message = create_message(sender, to, subject, message_txt)
            draft = create_draft(service, "me", message)

            if draft is None:
                return "Failed to create email draft"
            return f"Email sent successfully! Draft ID: {draft['id']}"
        except Exception as e:
            return f"An error occurred while sending email: {e}"
