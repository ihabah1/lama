from __future__ import annotations

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from . import services


@ensure_csrf_cookie
def home(request):
    return render(
        request,
        "analyzer/home.html",
        {
            "init_error": services.init_error,
            "approved_count": len(services.approved_combos),
        },
    )


@require_GET
def health(request):
    services.init_data()
    ok = services.init_error is None and len(services.approved_combos) > 0
    return JsonResponse(
        {
            "status": "ok" if ok else "degraded",
            "approved_combinations": len(services.approved_combos),
            "error": services.init_error,
        }
    )


@csrf_exempt
@require_POST
def check_numbers(request):
    services.init_data()
    data = services.parse_json_body(request)
    nums = sorted(int(x) for x in data.get("numbers", []))

    if len(nums) != 6:
        return JsonResponse(
            {"status": "error", "message": "יש לספק 6 מספרים"},
            status=400,
        )

    combo_tuple = tuple(nums)
    if combo_tuple in services.approved_combos:
        return JsonResponse(
            {
                "status": "approved",
                "message": "הצירוף מאושר! הוא נמצא במאגר הצירופים בעלי הפוטנציאל הגבוה.",
            }
        )
    reason = services.get_rejection_reason(nums)
    return JsonResponse({"status": "rejected", "message": reason})


@require_GET
def suggest_coverage(request):
    services.init_data()
    count = int(request.GET.get("count", "200"))
    suggestions = services.suggest_coverage(count)
    return JsonResponse({"suggestions": suggestions})


@require_GET
def suggest_top_stat(request):
    services.init_data()
    suggestions = services.suggest_top_stat(50)
    return JsonResponse({"top_statistical_suggestions": suggestions})


@require_GET
def suggest_diverse(request):
    services.init_data()
    suggestions = services.suggest_diverse(50)
    return JsonResponse({"diverse_suggestions": suggestions})
