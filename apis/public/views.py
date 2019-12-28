from json import dumps
from typing import List

from django.contrib.sessions.backends.base import SessionBase
from requests import Response as APIResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from externals.services import CreateReplyLineService
from games.services import DuaEmpatGeneratorService, DuaEmpatCalculatorService, DuaEmpatSolverService
from sessions.services import RetrieveSessionService


class WebhookAPI(APIView):

    def post(self, request: Request) -> Response:
        events = request.data['events']
        is_verification = events[0]['replyToken'] == '00000000000000000000000000000000'
        if not is_verification:
            self.forward_events(request, events)

        return Response(None, HTTP_200_OK)

    def forward_events(self, request: Request, events: list) -> List[APIResponse]:
        return [
            self.forward_event(request, event)
            for event in events
        ]

    def forward_event(self, request: Request, event: dict) -> APIResponse:
        source_type = event['source']['type']
        source_id = (
            event['source']['groupId'] if source_type == 'group' else
            event['source']['roomId'] if source_type == 'room' else
            event['source']['userId']
        )
        event_type = event['type']
        url = reverse(f'webhook-{source_type}-{event_type}-api', [source_id], request=request)
        session = RetrieveSessionService.run(source_id)

        return session.post(url, dumps(event))


class WebhookUserMessageAPI(APIView):
    def post(self, request: Request, user_id: str) -> Response:
        session = request.session
        event = request.data
        token = event['replyToken']
        message_type = event['message']['type']

        if message_type == 'text':
            text = event['message']['text']
            game = session.get('game', None)

            if game is None:
                messages = self.process_message(session, text)
                CreateReplyLineService.run(token, messages)
            elif game == 'DUA_EMPAT':
                messages = self.process_dua_empat_message(session, text)
                CreateReplyLineService.run(token, messages)

        return Response(None, HTTP_200_OK)

    def process_message(self, session: SessionBase, text: str) -> List[str]:
        if text == 'main 24':
            numbers = DuaEmpatGeneratorService.run()
            session['game'] = 'DUA_EMPAT'
            session['numbers'] = numbers
            return ['game dimulai', numbers.__str__()]

    def process_dua_empat_message(self, session: SessionBase, text: str) -> List[str]:
        if text == 'udahan':
            session.clear()
            return ['game selesai']
        elif text == 'ulang':
            numbers = session['numbers']
            return [numbers.__str__()]
        elif text == 'nyerah':
            numbers = session['numbers']
            answer = DuaEmpatSolverService.run(numbers) or 'tidak ada'
            numbers = DuaEmpatGeneratorService.run()
            session['numbers'] = numbers
            return [f'jawabannya {answer}', numbers.__str__()]
        elif text == 'tidak ada':
            numbers = session['numbers']
            answer = DuaEmpatSolverService.run(numbers)
            has_answer = answer is not None
            if has_answer:
                return ['ada jawabannya loh']
            else:
                numbers = DuaEmpatGeneratorService.run()
                session['numbers'] = numbers
                return ['tidak ada!!', numbers.__str__()]
        else:
            numbers = session['numbers']
            result = DuaEmpatCalculatorService.run(numbers, text)
            is_24 = result == 24
            if is_24:
                numbers = DuaEmpatGeneratorService.run()
                session['numbers'] = numbers
                return ['dua empat!!', numbers.__str__()]
            else:
                return [f'{text} hasilnya {result:g}']
