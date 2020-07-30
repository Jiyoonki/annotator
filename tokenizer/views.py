from django.shortcuts import render
from .models import Tokenoutput
from django.views.decorators.csrf import csrf_exempt
from konlpy.tag import Okt

import csv, io
from .models import Keywords, v1_Keywords, keyword_select
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Max, OuterRef, Subquery
from django.http import HttpResponse
from django.utils import timezone
from django.core import serializers
import json
# Create your views here.

def test(request):
    return render(request, 'tokenizer/test.html', {})


def keyword_selector(request):


    user_id = request.POST.get('input_user_id', '')
    next_type = request.POST.get('next_type', '')
    rand_order = request.POST.get('rand_order', '1')
    rand_order = int(rand_order)

    if user_id != '':
        if next_type == 'next':

            sql = 'select * ' \
                  'from tokenizer_keyword_select ' \
                  'where user_id = "' + user_id + '" ' \
                  'and (pos_keyword is null or neg_keyword is null) ' \
                  'order by rand() ' \
                  'limit 1 '

        elif next_type == 'previous':
            if rand_order == 1:
                minus_number = '0'
            else:
                minus_number = '1'

            sql = 'select * ' \
                  'from tokenizer_keyword_select ' \
                  'where user_id = "' + user_id + '" ' \
                  'and rand_order = ' + str(rand_order) + '-' + minus_number + ' ' \
                  'limit 1 '

        else:

            sql = 'select * ' \
                  'from tokenizer_keyword_select ' \
                  'where user_id = "' + user_id + '" ' \
                  'order by rand_order desc ' \
                  'limit 1 '


        data = keyword_select.objects.raw(sql)
        data = serializers.serialize('json', data, ensure_ascii=False)
        data = json.loads(data)[0]['fields']


        if next_type == 'next':
            table = keyword_select.objects.get(user_id=user_id, user_key=int(data['user_key']))
            table.updated_date = timezone.now()
            table.rand_order = rand_order + 1
            table.save()
            data['rand_order'] = str(rand_order + 1)

        if data['rand_order'] is None:
            table = keyword_select.objects.get(user_id=user_id, user_key=int(data['user_key']))
            table.updated_date = timezone.now()
            table.rand_order = 1
            table.save()
            data['rand_order'] = '1'


        for key, val in data.items():
            if val is None:
                data[key] = ''

        data['pos_text_norm_split'] = data['pos_text_norm'].split(' ')
        data['neg_text_norm_split'] = data['neg_text_norm'].split(' ')
        data['pos_keyword_split'] = data['pos_keyword'].split(' ')
        data['neg_keyword_split'] = data['neg_keyword'].split(' ')
        data['pos_word_num_split'] = [int(x) for x in data['pos_word_num'].split(' ') if x != '']
        data['neg_word_num_split'] = [int(x) for x in data['neg_word_num'].split(' ') if x != '']

    else:
        data = dict()
        data['rand_order'] = 1

    if request.method == "POST":
        print("POST requested")

        # if method == POST and submit name == submit_upload, insert csv file to database
        if 'submit_user_id' in request.POST:
            print("submit_user_id")
            print(request.POST.get('input_user_id', ''))

    content = {'user_id':user_id,
               'data':data}
    return render(request, 'tokenizer/keyword_selector.html', content)







def keyword_selector_update(request):
    user_id = request.GET.get('user_id')
    user_key = request.GET.get('user_key')
    type = request.GET.get('type')
    selected_keywords = request.GET.get('selected_keywords')
    selected_keywords_order = request.GET.get('selected_keywords_order')

    table = keyword_select.objects.get(user_id=user_id, user_key=user_key)
    table.updated_date = timezone.now()
    if type == "positive_words":
        table.pos_keyword = selected_keywords
        table.pos_word_num = selected_keywords_order
    elif type == "negative_words":
        table.neg_keyword = selected_keywords
        table.neg_word_num = selected_keywords_order

    table.save()

    return HttpResponse("Success!")
























text_dicts = []

def token_list(request):

    content = request.POST.get('content')
    if content is None:
        content = ""
    #if 'submit' in request.get:
    #    contents = ''.split(content)

    okt = Okt()
    text = okt.pos(content, norm = True, stem = True)
    output_text1 = [i[0] for i in text if
             ((i[1] not in ['Josa', 'Suffix', 'Punctuation']) &
              (i[0] not in ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ', 'ㅑ', 'ㅓ', 'ㅕ',
                            'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅔ', 'ㅖ', 'ㅐ', 'ㅒ', 'ㅠㅠ', 'ㅠㅠㅠ', 'ㅠㅠㅠㅠ', 'ㅋㅋ', 'ㅋㅋㅋ', 'ㅋㅋㅋㅋ','이','그','저','어느','매우','무척','너무','정말','진짜','되게']))]
    output_text = ' '.join(output_text1)

    output_text_dict = dict(zip(list(range(1, len(output_text1)+1)), output_text1))
    #text_dicts.append(output_text_dict)

    return render(request, 'tokenizer/token_list.html', {'content': content, 'output_text':output_text, 'output_text1':output_text1, 'output_text_dict':output_text_dict})






# keywords 또는 keywords/ url로 접속했을 경우 keywords/1/로 redirect 한다
def select_keywords_first_page(request):
    return select_keywords(request, current_page=1)

# keywords/<int:current_page> 또는 keywords/<int:current_page>/ url로 접속했을 경우
def select_keywords(request, current_page):

    # get key from input_key text box
    if request.POST.get('input_key', '') != '':
        key = request.POST.get('input_key', '')
        key = key.strip()
    elif request.GET.get('key', '') != '':
        key = request.GET.get('key', '')
    else:
        key = ''

    if request.method == "POST":
        print("POST requested")

        # if method == POST, set current_page = 1
        current_page = 1

        # if method == POST and submit name == submit_upload, insert csv file to database
        if 'submit_upload' in request.POST:
            print("submit_key")

        # if method == POST and submit name == submit_clear, delete all data corresponding to the current key
        elif 'submit_clear' in request.POST:
            print('submit_clear')
            Keywords.objects.filter(key=key).delete()

    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        print("GET requested")
        None

    # set number of data per page
    data_per_page = int(request.GET.get('data', '20'))
    start_data_index = (current_page - 1) * data_per_page + 1
    end_data_index = current_page * data_per_page

    # get total data count corresponding to the current key
    data_count = Keywords.objects.filter(key=key).count()
    total_pages = ((data_count - 1) // data_per_page) + 1
    page_list = list(range(total_pages + 1))[1:]

    # get data from database filtered by current key
    sql = 'select a.id, a.created_date, a.updated_date, a.`key`, a.key_index, a.text, a.words, a.words_selected, coalesce(a.keywords, "") as keywords ' \
          'from emotions.tokenizer_keywords a ' \
          'inner join(select id, row_number() over key_index as row_num ' \
          '           from emotions.tokenizer_keywords ' \
          '           where `key` = "' + key + '" ' \
          '           window key_index as (order by key_index)) b ' \
          'on a.id = b.id ' \
          'where b.row_num >= ' + str(start_data_index) + ' and b.row_num <= ' + str(end_data_index)

    data = Keywords.objects.raw(sql)

    # content is a context variable that can have different values depending on their context
    content = {'data': data,
               'key': key,
               'page_list': page_list,
               'current_page': current_page,
               'data_per_page': data_per_page
               }

    return render(request, 'tokenizer/select_keywords.html', content)

# select_keywords.html 에서 checkbox를 클릭했을 경우 데이터베이스 업데이트를 위해 호출됨
def ajax_update(request):
    if request.method == 'GET':
        print('ajax_update GET requested')

        keyword = Keywords.objects.get(key=request.GET.get('key'), key_index=request.GET.get('key_index'))
        keyword.words_selected = request.GET.get('words_selected')
        keyword.keywords = request.GET.get('keywords')
        keyword.updated_date = timezone.now()

        keyword.save()
        return HttpResponse("Success!")

    else:
        print('insertTest GET not requested')
        return HttpResponse("Request method is not a GET")


# key="" 일 때 select_keywords.html 에서 Download 버튼을 클릭했을 경우
def export_users_csv_no_key(request):
    return export_users_csv(request, "")

# select_keywords.html 에서 Download 버튼을 클릭했을 경우 데이터베이스 데이터를 csv 파일로 export 하기 위해 호출됨
def export_users_csv(request, key):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="keywords.csv"'

    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['Text', 'Keywords'])

    users = Keywords.objects.filter(key=key).values_list('text', 'keywords')
    for user in users:
        writer.writerow(user)

    return response

# keywords/upload 또는 keywords/upload/ url로 접속했을 경우
def upload_data(request):

    # get key from input_key text box
    key = request.POST.get('input_key', '')
    key = key.strip()

    data = ""
    data_count = ""
    if request.method == "POST":

        # if method == POST and submit name == submit_upload, insert csv file to database
        if 'submit_upload' in request.POST:

            # get csv file
            csv_file = request.FILES['file']

            # let's check if it is a csv file
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')
            data_set = csv_file.read().decode('UTF-8')

            # setup a stream which is when we loop through each line we are able to handle a data in a stream
            io_string = io.StringIO(data_set)
            next(io_string)

            # get max key_index corresponding to the current key
            # if None, set key_index = 1
            key_index = Keywords.objects.filter(key=key).aggregate(Max('key_index'))['key_index__max']
            if key_index is None:
                key_index = 1
            else:
                key_index = key_index + 1

            # insert csv to database
            bulk_list = []
            # read csv file
            for column in csv.reader(io_string, delimiter=',', quotechar='"'):
                # tokenizing with konlpy package
                okt = Okt()
                tokens = okt.pos(column[0], norm=True, stem=True)
                words = [i[0] for i in tokens if
                                ((i[1] not in ['Josa', 'Suffix', 'Punctuation']) &
                                 (i[0] not in ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ',
                                               'ㅑ', 'ㅓ', 'ㅕ',
                                               'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅔ', 'ㅖ', 'ㅐ', 'ㅒ', 'ㅠㅠ', 'ㅠㅠㅠ', 'ㅠㅠㅠㅠ', 'ㅋㅋ', 'ㅋㅋㅋ',
                                               'ㅋㅋㅋㅋ', '이', '그', '저', '어느', '매우', '무척', '너무', '정말', '진짜', '되게']))]
                words = ' '.join(words)
                # create Keywords object and store it in bulk_list
                bulk_list.append(Keywords(key=key, key_index=key_index, text=column[0], words=words))
                key_index = key_index + 1
            # insert all data to Keywords table at once
            Keywords.objects.bulk_create(bulk_list)

            data_count = Keywords.objects.filter(key=key).count()

        # if method == POST and submit name == submit_key, get count by key
        elif 'submit_key' in request.POST:
            data_count = Keywords.objects.filter(key=key).count()

        # if method == POST and submit name == submit_all, get all key, count data
        elif 'submit_all' in request.POST:
            # get data count group by key
            sql = 'select 1 as id, `key`, count(*) as cnt ' \
                  'from emotions.tokenizer_keywords ' \
                  'group by `key` ' \
                  'order by `key` '
            data = Keywords.objects.raw(sql)

        # if method == POST and submit name == submit_delete, delete by key
        elif 'submit_delete' in request.POST:
            Keywords.objects.filter(key=key).delete()

        # if method == POST and submit name == submit_delete_all, delete all data
        elif 'submit_delete_all' in request.POST:
            Keywords.objects.all().delete()

    # content is a context variable that can have different values depending on their context
    content = {'key': key,
               'data_count': data_count,
               'data': data}

    return render(request, 'tokenizer/upload_data.html', content)







# ---------------------- v1 ------------------------------

def v1_select_keywords_first_page(request):
    return v1_select_keywords(request, current_page=1)


def v1_select_keywords(request, current_page):

    # get session_id
    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key

    if request.method == "POST":
        print("POST requested")

        # if method == POST, set current_page = 1
        current_page = 1

        # if method == POST and submit name == submit_upload, insert csv file to database
        if 'submit_upload' in request.POST:
            print("submit_upload")

            # get csv file
            csv_file = request.FILES['file']

            # let's check if it is a csv file
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')
            data_set = csv_file.read().decode('UTF-8')

            # setup a stream which is when we loop through each line we are able to handle a data in a stream
            io_string = io.StringIO(data_set)
            next(io_string)

            # get max session_index in current session
            # if None, set session_index = 1
            session_index = v1_Keywords.objects.filter(session_id=session_id).aggregate(Max('session_index'))['session_index__max']
            if session_index is None:
                session_index = 1
            else:
                session_index = session_index + 1

            # insert csv to database
            bulk_list = []
            # read csv file
            for column in csv.reader(io_string, delimiter=',', quotechar='"'):
                # tokenizing with konlpy package
                okt = Okt()
                tokens = okt.pos(column[0], norm=True, stem=True)
                words = [i[0] for i in tokens if
                                ((i[1] not in ['Josa', 'Suffix', 'Punctuation']) &
                                 (i[0] not in ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ',
                                               'ㅑ', 'ㅓ', 'ㅕ',
                                               'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅔ', 'ㅖ', 'ㅐ', 'ㅒ', 'ㅠㅠ', 'ㅠㅠㅠ', 'ㅠㅠㅠㅠ', 'ㅋㅋ', 'ㅋㅋㅋ',
                                               'ㅋㅋㅋㅋ', '이', '그', '저', '어느', '매우', '무척', '너무', '정말', '진짜', '되게']))]
                words = ' '.join(words)
                # create Keywords object and store it in bulk_list
                bulk_list.append(v1_Keywords(session_id=session_id, session_index=session_index, text=column[0], words=words))
                session_index = session_index + 1
            # insert all data to Keywords table at once
            v1_Keywords.objects.bulk_create(bulk_list)

        # if method == POST and submit name == submit_clear, delete all data in current session
        elif 'submit_clear' in request.POST:
            print('submit_clear')
            v1_Keywords.objects.filter(session_id=session_id).delete()

    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        print("GET requested")
        None

    # set number of data per page
    data_per_page = int(request.GET.get('data', '20'))
    start_data_index = (current_page - 1) * data_per_page + 1
    end_data_index = current_page * data_per_page

    # get total data count in current session
    data_count = v1_Keywords.objects.filter(session_id=session_id).count()
    total_pages = ((data_count - 1) // data_per_page) + 1
    page_list = list(range(total_pages + 1))[1:]

    # get data from database filtered by current session id
    sql = 'select a.id, a.created_date, a.updated_date, a.session_id, a.session_index, ' \
          '       a.text, a.words, a.words_selected, coalesce(a.keywords, "") as keywords ' \
          'from tokenizer_v1_keywords a ' \
          'inner join (select id, row_number() over session_index as row_num ' \
          '            from emotions.tokenizer_v1_keywords' \
          '            where session_id = "' + session_id + '" ' \
          '            window session_index as (order by session_index)) b ' \
          'on a.id = b.id ' \
          'where b.row_num >= ' + str(start_data_index) + ' and b.row_num <= ' + str(end_data_index)
    
    data = v1_Keywords.objects.raw(sql)

    # content is a context variable that can have different values depending on their context
    content = {'data': data,
               'session_id': session_id,
               'page_list': page_list,
               'current_page': current_page,
               'data_per_page': data_per_page
               }

    return render(request, 'tokenizer/v1_select_keywords.html', content)


def v1_ajax_update(request):
    if request.method == 'GET':
        print('ajax_update GET requested')

        keyword = v1_Keywords.objects.get(session_id=request.GET.get('session_id'), session_index=request.GET.get('session_index'))
        keyword.words_selected = request.GET.get('words_selected')
        keyword.v1_keywords = request.GET.get('keywords')
        keyword.updated_date = timezone.now()

        keyword.save()
        return HttpResponse("Success!")

    else:
        print('insertTest GET not requested')
        return HttpResponse("Request method is not a GET")



def v1_export_users_csv(request, session_id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="keywords.csv"'

    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['Text', 'Keywords'])

    users = v1_Keywords.objects.filter(session_id=session_id).values_list('text', 'keywords')
    for user in users:
        writer.writerow(user)

    return response