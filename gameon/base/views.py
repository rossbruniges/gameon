from django.shortcuts import render


def action_unavailable_response(request, case=None,
                                template_name="403.html"):
    """Generic page for unavailable actions"""
    context = {'case': case}
    return render(request, template_name, context, status=403)
