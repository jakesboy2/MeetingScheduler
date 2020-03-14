from django.shortcuts import render, redirect
from django.views.generic import View
from meeting.views import get_meetings_by_user
from meeting.views import pull_profile

from .. import models

def availability(request):
    if not request.user.is_authenticated:
            return redirect('LoginProcess')
    
    user = request.user if request.user.is_authenticated else None
    
    if user is None:
        return redirect('LoginProcess')

    meeting_list = get_meetings_by_user(user)
    avlb_meeting_list = []
    
    # Get avlb counts
    for meeting in meeting_list:
        avlb_count = models.TimeAvailability.objects.filter(meeting_id=meeting.id).count()
        avlb_meeting_list.append({'meeting': meeting, 'avlb_count': avlb_count})

    context = {
        'meeting_list': avlb_meeting_list,
    }

    return render(request, 'availability/index.html', context)


class Availability(View):
    def get(self, request, meeting_id):
      
        if not request.user.is_authenticated:
            return redirect('LoginProcess')

        user = request.user if request.user.is_authenticated else None
        
        if user is None:
            return redirect('LoginProcess')

        meeting_list = get_meetings_by_user(user)
        active_meeting = [meeting for meeting in meeting_list if meeting.id == meeting_id][0]
        avlb_meeting_list = []

        # Get avlb counts
        for meeting in meeting_list:
            avlb_count = models.TimeAvailability.objects.filter(meeting_id=meeting.id).count()
            avlb_meeting_list.append({'meeting': meeting, 'avlb_count': avlb_count})

        app_url = request.path
        # time_slots = models.TimeAvailability.objects.filter(meeting=meeting_id)
        time_slots = models.TimeAvailability.objects.raw('select * from meeting_timeavailability where meeting_id = %s', [meeting_id])
        json_data = models.TimeAvailability.objects.all();

        time_slots_json = "["
        for datum in json_data:
            meeting = '"meeting":{"id":"' + str(datum.meeting.id) + '","description":"' + datum.meeting.description + '"}';
            time_slots_json += '{"id":"' + str(datum.id) + '","start_time":"' + str(datum.start_time) + '","end_time":"' + str(datum.end_time) + '",' + meeting + '},';
        if len(time_slots_json) > 1:
            time_slots_json = time_slots_json[:-1]
        time_slots_json += ']';
        
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(time_slots_json);

        context = {
            'active_meeting': active_meeting,
            'meeting_list': avlb_meeting_list,
            'app_url': app_url,
            'time_slots': time_slots,
            'time_slots_json': time_slots_json
        }
        
        return render(request, 'availability/meeting_availability.html', context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('LoginProcess')

        user = request.user if request.user.is_authenticated else None        
        
        if user is None:
            return redirect('LoginProcess')

        profile = pull_profile(user)

        start_time = request.POST.get('start_time') if request.POST.get('start_time') else None
        end_time = request.POST.get('end_time') if request.POST.get('end_time') else None
        meeting_id = kwargs.get('meeting_id') if kwargs.get('meeting_id') else None

        # meetingId = request.POST.get('meeting_id')
        meeting = models.Meeting.objects.get(id=meeting_id) if models.Meeting.objects.get(id=meeting_id) else None
        app_url = request.path

        context = {
            'meeting_list': [],
            'active_meeting': meeting,
            'app_url': app_url,
            'success': True,
            'errors': dict(),
            'time_slots': None,
            'time_slots_json': None
        }
        
        if start_time is None:
            context["success"] = False
            context["errors"]["start_time"] = True
        if end_time is None:
            context["success"] = False
            context["errors"]["end_time"] = True

        if context["success"]:
            models.TimeAvailability.objects.create(start_time=start_time,
                                                end_time=end_time,
                                                meeting=meeting,
                                                user=profile)

        meeting_list = get_meetings_by_user(user)
        avlb_meeting_list = []

        # Get avlb counts
        for meeting in meeting_list:
            avlb_count = models.TimeAvailability.objects.filter(meeting_id=meeting.id).count()
            avlb_meeting_list.append({'meeting': meeting, 'avlb_count': avlb_count})
            
        time_slots = models.TimeAvailability.objects.filter(meeting=meeting_id)
        
        json_data = models.TimeAvailability.objects.all();
        time_slots_json = "["
        for datum in json_data:
            meeting = '"meeting":{"id":"' + str(datum.meeting.id) + '","description":"' + datum.meeting.description + '"}';
            time_slots_json += '{"id":"' + str(datum.id) + '","start_time":"' + str(datum.start_time) + '","end_time":"' + str(datum.end_time) + '",' + meeting + '},';
        if len(time_slots_json) > 1:
            time_slots_json = time_slots_json[:-1]
        time_slots_json += ']';

        context['meeting_list'] = avlb_meeting_list
        context['time_slots'] = time_slots
        context['time_slots_json'] = time_slots_json

        return render(request, 'availability/meeting_availability.html', context)

class AvailabilityDelete(View):
    def post(self, request, *args, **kwargs):
        user = request.user if request.user.is_authenticated else None        
        
        if user is None:
            return redirect('LoginProcess')
        
        aid = request.POST.get('id') if request.POST.get('id') else None
        slot = models.TimeAvailability.objects.get(id=aid)
        slot.delete()

        meeting_id = kwargs.get('meeting_id') if kwargs.get('meeting_id') else None
        # meetingId = request.POST.get('meeting_id')
        meeting = models.Meeting.objects.get(id=meeting_id) if models.Meeting.objects.get(id=meeting_id) else None

        meeting_list = get_meetings_by_user(user)
        avlb_meeting_list = []

        # Get avlb counts
        for meeting in meeting_list:
            avlb_count = models.TimeAvailability.objects.filter(meeting_id=meeting.id).count()
            avlb_meeting_list.append({'meeting': meeting, 'avlb_count': avlb_count})
            
        active_meeting = meeting
        app_url = request.path
        time_slots = models.TimeAvailability.objects.filter(meeting=meeting_id)
        
        json_data = models.TimeAvailability.objects.all();
        time_slots_json = "["
        for datum in json_data:
            meeting = '"meeting":{"id":"' + str(datum.meeting.id) + '","description":"' + datum.meeting.description + '"}';
            time_slots_json += '{"id":"' + str(datum.id) + '","start_time":"' + str(datum.start_time) + '","end_time":"' + str(datum.end_time) + '",' + meeting + '},';
        if len(time_slots_json) > 1:
            time_slots_json = time_slots_json[:-1]
        time_slots_json += ']';

        context = {
            'meeting_list': avlb_meeting_list,
            'active_meeting': active_meeting,
            'app_url': app_url,
            'time_slots': time_slots,
            'time_slots_json': time_slots_json
        }

        return render(request, 'availability/meeting_availability.html', context)
    