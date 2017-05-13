# -*- coding: utf-8 -*-

import sys
import json
from pprint import pprint
from datetime import datetime
from croniter import croniter

APIKEY = '4b9d31c7111d440fa86e606c6f846a18'
PROJECT = '190405'

jobs = [{
    'schedules': (
        '0 8,12,17 * * MON,TUE,WED,THU,FRI',
        '0 12,18 * * SAT,SUN',
    ),
    # FIXME get spider name from ze/spider/*
    'spiders': ('cartacapital', 'correiobraziliense', 'estadao', 'estadodeminas',
                'folhadesp', 'g1', 'gestaoescolar', 'ig', 'novaescola', 'uol',
                'veja'),
    'search_arg_template': {
        "query": None, 
        "engine": "google", 
        "last_update": "d", 
        "results_per_page": 50, 
        "pages": 2,
    },
    'search_arg_keywords': ({
        'query': 'Celpe-Bras OR "Certificado * Proficiência * Língua Portuguesa"',
        'tags': ('Ações Internacionais', 'CELPE-Bras')
    },{
        'query': 'Pisa OR "Programme * International Student Assessment"',
        'tags': ('Ações Internacionais', 'Pisa')
    },{
        'query': 'EAG OR "Education * Glance"',
        'tags': ('Ações Internacionais', 'EAG')
    },{
        'query': 'TALIS OR "Pesquisa Internacional sobre Ensino * Aprendizagem" OR "Teaching and Learning International Survey"',
        'tags': ('Ações Internacionais', 'TALIS')
    },{
        'query': 'Enem OR "Exame Nacional * Ensino Médio"',
        'tags': ('Educação Básica', 'Enem')
    },{
        'query': '"Prova Brasil" OR "Avaliação Nacional * Rendimento Escolar"',
        'tags': ('Educação Básica', 'Prova Brasil')
    },{
        'query': '"Provinha Brasil"',
        'tags': ('Educação Básica', 'Provinha Brasil')
    },{
        'query': 'ANA OR "Avaliação Nacional * Alfabetização"',
        'tags': ('Educação Básica', 'ANA')
    },{
        'query': 'Aneb OR "Avaliação Nacional * Educação Básica"',
        'tags': ('Educação Básica', 'Aneb')
    },{
        'query': 'Saeb OR "Sistema Nacional * Avaliação * Educação Básica"',
        'tags': ('Educação Básica', 'Saeb')
    },{
        'query': 'Anresc OR "Avaliação Nacional * Rendimento Escolar"',
        'tags': ('Educação Básica', 'Anresc')
    },{
        'query': 'Encceja OR "Exame Nacional * Certificação * Competências * Jovens * Adultos" OR "Certificação * Competências * Jovens * Adultos"',
        'tags': ('Educação Básica', 'Encceja')
    },{
        'query': 'Educacenso OR "Censo Escolar * Educação Básica"',
        'tags': ('Educação Básica', 'Educacenso')
    },{
        'query': 'Revalida OR "Exame Nacional * Revalidação * Diplomas Médicos"',
        'tags': ('Educação Superior', 'Revalida')
    },{
        'query': 'AnaSEM OR "Avaliação Nacional Seriada * Estudantes * Medicina"',
        'tags': ('Educação Superior', 'AnaSEM')
    },{
        'query': 'ENADE OR "Exame Nacional * Desempenho * Estudantes"',
        'tags': ('Educação Superior', 'ENADE')
    },{
        'query': 'Sinaes OR "Sistema Nacional * Avaliação * Educação Superior"',
        'tags': ('Educação Superior', 'Sinaes')
    },{
        'query': 'BASIs OR "Banco * Avaliadores * Sistema Nacional * Avaliação * Educação Superior" IR "Banco * Avaliadores"',
        'tags': ('Educação Superior', 'BASIs')
    },{
        'query': '"Avaliação * Curso* * Graduação"',
        'tags': ('Educação Superior', 'Termo', 'Avaliação * Curso* * Graduação')
    },{
        'query': '"Censo * Educação Superior"',
        'tags': ('Educação Superior', 'Censo * Educação Superior')
    },{
        'query': 'Inep OR "Instituto Nacional * Estudos * Pesquisas Educacionais Anísio Teixeira"',
        'tags': ('Institucional', 'Organização', 'Inep')
    },{
        'query': 'Cibec OR "Centro * Informação * Biblioteca * Educação"',
        'tags': ('Institucional', 'Organização', 'Cibec')
    },{
        'query': '"Maria Inês Fini"',
        'tags': ('Institucional', 'Pessoa', "Maria Inês Fini")
    },{
        'query': '"Luana Bergmann Soares"',
        'tags': ('Institucional', 'Pessoa', 'Luana Bergmann Soares')
    },{
        'query': '"Carlos Eduardo Moreno Sampaio"',
        'tags': ('Institucional', 'Pessoa', 'Carlos Eduardo Moreno Sampaio')
    },{
        'query': '"Eunice de Oliveira Ferreira Santos"',
        'tags': ('Institucional', 'Pessoa', 'Eunice de Oliveira Ferreira Santos')
    },{
        'query': '"Valdir QuintAna Gomes Junior"',
        'tags': ('Institucional', 'Pessoa', 'Valdir QuintAna Gomes Junior')
    },{
        'query': '"Camilo Mussi"',
        'tags': ('Institucional', 'Pessoa', '"Camilo Mussi"')
    },{
        'query': 'Rui Barbosa Brito Júnior',
        'tags': ('Institucional', 'Pessoa', 'Rui Barbosa Brito Júnior')
    },{
        'query': '"Avaliações Educacionais"',
        'tags': ('Termo', 'Avaliações Educacionais')
    },{
        'query': '"Avaliação Educacional"',
        'tags': ('Termo', 'Avaliação Educacional')
    })
}]

def main(argv):
    jobs_file = open('./jobs.jl', mode='w+')
        
    for job in jobs:
        for cron_notation in job['schedules']:
            minutes, hours, days, months, days_of_week = cron_notation.split()
            n_minutes = len(minutes.split(','))
            n_hours = len(hours.split(','))
            n_days = len(days.split(','))
            n_months = len(months.split(','))
            n_days_of_week = len(days_of_week.split(','))
            cron_iter = croniter(cron_notation)
            number_of_periodic_jobs = 0
            
            for i in range(0, n_minutes*n_hours*n_days*n_months*n_days_of_week):
                date_time = cron_iter.get_next(datetime)
                day_of_week = '7' if date_time.weekday() == 0 else str(date_time.weekday())
                
                for keyword in job['search_arg_keywords']:
                    periodic_job = {
                        'description': '',
                        'addtags': keyword['tags'],
                        'minutes_shift': '{d.minute}'.format(d=date_time),
                        'hour': date_time.strftime('%H').lstrip('0'),
                        'day': '*' if days_of_week == '*' else day_of_week,
                        'dayofmonth': '*' if days == '*' else str(date_time.day()),
                        'month': '*' if months == '*' else str(date_time.month()),
                        'spiders': []
                    }
                    
                    for job_spider in job['spiders']:
                        spider = {
                            'name': job_spider,
                            'spider_args': {
                                'search': json.dumps({
                                    'query': keyword['query'],
                                    'engine': 'google', 
                                    'last_update': 'd', 
                                    'results_per_page': 50, 
                                    'pages': 2,
                                }, ensure_ascii=False)
                            },
                            'priority': 2,
                        }
                        periodic_job['spiders'].append(spider)
                        number_of_periodic_jobs += 1
                        sys.stdout.write('Number of Period Jobs: %d\r'%number_of_periodic_jobs)
                        sys.stdout.flush()
                    
                    jobs_file.writelines((json.dumps(periodic_job, ensure_ascii=False), '\n'))
    jobs_file.close()

if __name__ == '__main__':
   main(sys.argv[1:])