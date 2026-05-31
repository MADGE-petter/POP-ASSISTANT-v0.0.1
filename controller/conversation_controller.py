"""Conversation Controller - Điều phối conversation flow."""

from typing import Callable, Optional

from controller.interfaces import (
    IActionHandler,
    IAudioService,
    ISqlService,
    IUserController,
)
from service.conversation_flow_service import ConversationFlowService


class ConversationController:
    def __init__(
        self,
        audio_service: IAudioService,
        sql_service: ISqlService,
        action_handler: IActionHandler,
        user_controller: IUserController,
        interactive_alert_service=None,
    ):
        self.flow_service = ConversationFlowService(
            audio_service,
            sql_service,
            action_handler,
            user_controller,
            interactive_alert_service,
        )

    def init_intent_service(self):
        self.flow_service.init_intent_service()

    def start_session(self) -> None:
        self.flow_service.start_session()

    def end_session(self) -> None:
        self.flow_service.end_session()

    def run_main_loop(
        self,
        get_input_callback: Callable[[], Optional[str]],
        on_idle_callback: Optional[Callable] = None,
        idle_timeout: int = 15,
    ) -> None:
        self.flow_service.run_main_loop(
            get_input_callback=get_input_callback,
            on_idle_callback=on_idle_callback,
            idle_timeout=idle_timeout,
        )

    def run_first_interaction(
        self,
        get_input_callback: Callable[[], Optional[str]],
        speak_callback: Optional[Callable] = None,
        from_wake_up: bool = False,
    ) -> None:
        self.flow_service.run_first_interaction(
            get_input_callback=get_input_callback,
            speak_callback=speak_callback,
            from_wake_up=from_wake_up,
        )

    def stop(self) -> None:
        self.flow_service.stop()

    def set_assistant_active(self, active: bool) -> None:
        self.flow_service.set_assistant_active(active)
