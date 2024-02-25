import random

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import Teacher
import csv

class Whos_hotter(View):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.total_count = Teacher.objects.all().count()

    def get_random_teacher(self):
        return random.randint(1, self.total_count)

    def get(self, request):
        right = Teacher.objects.filter(pk=self.get_random_teacher()).get()
        left = Teacher.objects.filter(pk=self.get_random_teacher()).get()
        extra_context = {
            'title': 'Самый горячий препод ижгту',
            'right_img': right.pict,
            'left_img': left.pict,
            'right_name': right.name,
            'left_name': left.name,
            'novigation_url': 'rating',
            'novigation_name': 'рейтинг',
            'right_id': right.pk,
            'left_id': left.pk,
            'right_link': f'https://istu.ru/staff/{right.site_id}',
            'left_link': f'https://istu.ru/staff/{left.site_id}',
        }
        return render(request, 'chooser/index.html', context=extra_context)

    def post(self, request):
        post = request.POST
        up_id, down_id = post['action'].split()
        up_teacher = Teacher.objects.filter(id=up_id).get()
        down_teacher = Teacher.objects.filter(id=down_id).get()
        print(up_teacher)

        up_teacher.rating+=1
        down_teacher.rating-=1
        up_teacher.save()
        down_teacher.save()

        return self.get(request)


class Rating(ListView):
    def get(self, request):
        extra_context = {
            'tops': Teacher.objects.order_by('rating')[:10],
            'novigation_url': 'whos_hotter' ,
            'novigation_name': 'Главная'
        }
        return render(request, 'chooser/rating.html', context=extra_context)


class Full_bd(View):
    def get(self, request):
        with open('chooser\data\data.csv', 'r', encoding ='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if row:
                    site_id = row[0]
                    name = row[1]
                    pict = row[2]
                    descr = row[3]
                    Teacher.objects.create(site_id=site_id, name = name, pict = pict, description = descr, rating = 0)

        return HttpResponse(request, 'Succsess')

class Update_bd(View):
    def get(self, request):
        with open('chooser\data\data.csv', 'r', encoding ='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if row:
                    site_id = row[0]
                    name = row[1]
                    Teacher.objects.filter(name=name).update(site_id=site_id) #что обновлять

        return HttpResponse(request, 'Succsess')
