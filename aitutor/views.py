from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.conf import settings

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

@login_required
@require_http_methods(["GET", "POST"])
def ai_teacher_chat(request):
    answer = None
    question = None
    error = None

    if request.method == "POST":
        question = request.POST.get("question", "").strip()
        if question:
            if OpenAI is None or not settings.OPENAI_API_KEY:
                error = "AI backend is not configured. Please set OPENAI_API_KEY on the server."
            else:
                try:
                    client = OpenAI(api_key=settings.OPENAI_API_KEY)
                    chat_completion = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are an encouraging study coach for N.O.K (Network of Knowledge). "
                                    "You teach step-by-step, always ask short check questions, and keep the student motivated. "
                                    "You use learning psychology: reduce anxiety, celebrate small wins, and keep students in flow. "
                                    "Your style is friendly, simple, and focused on helping Uzbek students succeed in math, languages and exams."
                                ),
                            },
                            {"role": "user", "content": question},
                        ],
                    )
                    answer = chat_completion.choices[0].message.content
                except Exception as e:
                    error = f"AI error: {e}"

    return render(
        request,
        "aitutor/chat.html",
        {"answer": answer, "question": question, "error": error},
    )
