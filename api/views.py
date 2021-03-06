from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db.models import Q

from main.models import StudyField
from main.models import Course
from main.models import Section
from main.models import Announcement
from main.models import Material
from main.models import Lecturer

# Create your views here.
def index(request):
	return HttpResponse("Welcome to aau push APIs.")

def study_fields(request):
	all_study_fields = StudyField.objects.all()

	#JSON output
	#Start json array
	output = "[";

	# Loop through every study field and add them as a json object
	for study_field in all_study_fields:
		output += "{"
		output += "\"id\":" + str(study_field.id) + ","
		output += "\"name\":" + "\"" + study_field.name + "\"" + ","
		output += "\"code\":" + "\"" + study_field.code + "\""
		output += "},"

	# remove the last list separator comma
	output = output[::-1].replace(",", "", 1)[::-1]

	#end of json array
	output += "]"


	return HttpResponse(output, content_type='application/json')

def courses(request):
	# Check if study_field exists, exit if it doesn't
	if request.GET.get('study_field'):
		study_field_id = int(request.GET.get('study_field'))
	else :
		return HttpResponse("Incorrect API request format. Refer to the docmumentaion.")

	if request.GET.get('section'):
		section_code = request.GET.get('section')
		section = get_object_or_404(Section, code=section_code)
		courses = Course.objects.filter(section = section).filter(studyfield__id=study_field_id)
	elif request.GET.get('ex_section'):
		section_code = request.GET.get('ex_section')
		section = get_object_or_404(Section, code=section_code)
		courses = Course.objects.exclude(section = section).filter(studyfield__id=study_field_id)
	else:
		courses = Course.objects.filter(studyfield__id=study_field_id)


	#JSON output
	#Start json array
	output = "[";

	# Loop through every study field and add them as a json object
	for course in courses:
		output += "{"
		output += "\"id\":" + str(course.id) + ","
		output += "\"name\":" + "\"" + course.name + "\"" #+ ","
		#output += "\"code\":" + "\"" + study_field.code + "\""
		output += "},"

	# remove the last list separator comma
	output = output[::-1].replace(",", "", 1)[::-1]

	#end of json array
	output += "]"

	return HttpResponse(output, content_type='application/json')

def announcements(request):
	#filter query
	query = Q()
	if request.GET.get('sections'):
		section_codes = request.GET.get('sections').split('-')
		for section_code in section_codes:
			section = get_object_or_404(Section, code=section_code)
			query.add(Q(section=section), Q.OR)
	elif request.GET.get('course_section'):
		course_section_list = request.GET.get('course_section').split('-')
		for course_section in course_section_list:
			course = get_object_or_404(Course, pk=int(course_section.split(':')[0]))
			section = get_object_or_404(Section, code=course_section.split(':')[-1])
			lecturers = Lecturer.objects.filter(course=course)
			if len(lecturers) < 1:
				continue
			for lecturer in lecturers:
				query.add(Q(lecturer = lecturer,section=section), Q.OR)
	else:
		return HttpResponse("Incorrect API request format. Refer to the docmumentaion.")
	# Apply filter
	announcements = Announcement.objects.filter(query).order_by('-pub_date').distinct()
	if request.GET.get('id'):
		announcements = announcements.filter(id__gt=int(request.GET.get('id')))

	#JSON output
	#Start json array
	output = "[";

	for announcement in announcements:
		output += "{"
		output += "\"id\":" + str(announcement.id) + ","
		output += "\"message\":" + "\"" + announcement.message + "\"" + ","
		output += "\"lecturer_name\":" + "\"" + announcement.lecturer.name + "\"" + ","
		output += "\"post_date\":" + "\"" + str(announcement.pub_date) + "\"" + ","
		output += "\"exp_date\":" + "\"" + str(announcement.exp_date) + "\"" + ","
		output += "\"file_one\":" + "\"" + str(announcement.get_link_one()) + "\"" + ","
		output += "\"file_two\":" + "\"" + str(announcement.get_link_two()) + "\"" + ","
		output += "\"is_urgent\":" + str(int(announcement.is_urgent))  #+ ","
		output += "},"

	# remove the last list separator comma
	output = output[::-1].replace(",", "", 1)[::-1]

	#end of json array
	output += "]"

	return HttpResponse(output, content_type='application/json')

def materials(request):
	#Filter query
	query = Q()
	if request.GET.get('course_section'):
		course_section_list = request.GET.get('course_section').split('-')
		for course_section in course_section_list:
			course = get_object_or_404(Course, pk=int(course_section.split(':')[0]))
			section = get_object_or_404(Section, code=course_section.split(':')[-1])
			query.add(Q(section=section,course=course),Q.OR)
	elif request.GET.get('sections'):
		section_codes = request.GET.get('sections').split('-')
		for section_code in section_codes:
			section = get_object_or_404(Section, code = section_code)
			query.add(Q(section=section),Q.OR)
	elif request.GET.get('courses'):
		course_ids = request.GET.get('courses').split('-')
		for course_id in course_ids:
			course = get_object_or_404(Course, pk=int(course_id))
			query.add(Q(course=course), Q.OR)
	else:
		return HttpResponse("Incorrect API request format. Refer to the docmumentaion.")
	#Apply filter
	materials = Material.objects.filter(query).order_by('-pub_date').distinct()
	if request.GET.get('id'):
		materials = materials.filter(id__gt=int(request.GET.get('id')))

	#JSON output
	#Start json array
	output = "[";

	for material in materials:
		output += "{"
		output += "\"id\":" + str(material.id) + ","
		output += "\"name\":" + "\"" + material.name + "\"" + ","
		output += "\"description\":" + "\"" + material.description + "\"" + ","
		output += "\"pub_date\":" + "\"" + str(material.pub_date) + "\"" + ","
		output += "\"file_format\":" + "\"" + material.ext() + "\"" + ","
		output += "\"file_size\":" + str(material.file_size()) + ","
		output += "\"course_id\":" + str(material.course.id)
		output += "},"

	# remove the last list separator comma
	output = output[::-1].replace(",", "", 1)[::-1]

	#end of json array
	output += "]"

	return HttpResponse(output, content_type='application/json')

def section_exists(request):
	section_code = request.GET.get('section_code')

	if Section.objects.filter(code=section_code).count() < 1:
		return HttpResponse("false")
	else:
		return HttpResponse("true")

def sections(request):
	study_field = get_object_or_404(StudyField, pk=int(request.GET.get('study_field_id')))

	sections = Section.objects.filter(studyfield = study_field)

	#JSON output
	#Start json array
	output = "[";

	for section in sections:
		output += "{"
		output += "\"code\":" + section.code
		output += "},"

	# remove the last list separator comma
	output = output[::-1].replace(",", "", 1)[::-1]

	#end of json array
	output += "]"

	return HttpResponse(output, content_type='application/json')
