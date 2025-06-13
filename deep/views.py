from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Feedback
import json

@csrf_exempt
def submit_feedback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')

            if not (name and email and message):
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            feedback = Feedback.objects.create(
                name=name,
                email=email,
                message=message
            )

            return JsonResponse({'message': 'Feedback submitted successfully!'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)


def get_all_feedback(request):
    if request.method == 'GET':
        feedbacks = Feedback.objects.all().order_by('-submitted_at')
        data = []

        for feedback in feedbacks:
            data.append({
                'id': feedback.id,
                'name': feedback.name,
                'email': feedback.email,
                'message': feedback.message,
                'submitted_at': feedback.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
            })

        return JsonResponse({'feedbacks': data}, safe=False)

    return JsonResponse({'error': 'Only GET method allowed'}, status=405)