import sys
import json
from datetime import datetime, timezone
from scrapy.commands import ScrapyCommand
from croniter import croniter

# -*- coding: utf-8 -*-

jobs = [{
    'schedules': (
        '0 8,12,17 * * MON,TUE,WED,THU,FRI',
        '0 12,18 * * SAT,SUN',
    ),
    # FIXME get spider name from ze/spider/*
    'spiders': ('cartacapital', 'correiobraziliense', 'estadao', 'estadodeminas',
                'folhadesp', 'g1', 'gestaoescolar', 'ig', 'novaescola', 'uol',
                'veja'),
    'search_arg_keywords': ({
        'query': 'Celpe-Bras OR "Certificado * Proficiência * Língua Portuguesa"',
        'tags': ('Ações Internacionais', 'CELPE-Bras'),
        'priority': 60,
    },{
        'query': 'Pisa OR "Programme * International Student Assessment"',
        'tags': ('Ações Internacionais', 'Pisa'),
        'priority': 60,
    },{
        'query': 'EAG OR "Education * Glance"',
        'tags': ('Ações Internacionais', 'EAG'),
        'priority': 60,
    },{
        'query': 'TALIS OR "Pesquisa Internacional sobre Ensino * Aprendizagem" OR "Teaching and Learning International Survey"',
        'tags': ('Ações Internacionais', 'TALIS'),
        'priority': 60,
    },{
        'query': 'Enem OR "Exame Nacional * Ensino Médio"',
        'tags': ('Educação Básica', 'Enem'),
        'priority': 60,
    },{
        'query': '"Prova Brasil" OR "Avaliação Nacional * Rendimento Escolar"',
        'tags': ('Educação Básica', 'Prova Brasil'),
        'priority': 50,
    },{
        'query': '"Provinha Brasil"',
        'tags': ('Educação Básica', 'Provinha Brasil'),
        'priority': 50,
    },{
        'query': 'ANA OR "Avaliação Nacional * Alfabetização"',
        'tags': ('Educação Básica', 'ANA'),
        'priority': 50,
    },{
        'query': 'Aneb OR "Avaliação Nacional * Educação Básica"',
        'tags': ('Educação Básica', 'Aneb'),
        'priority': 50,
    },{
        'query': 'Saeb OR "Sistema Nacional * Avaliação * Educação Básica"',
        'tags': ('Educação Básica', 'Saeb'),
        'priority': 50,
    },{
        'query': 'Anresc OR "Avaliação Nacional * Rendimento Escolar"',
        'tags': ('Educação Básica', 'Anresc'),
        'priority': 40,
    },{
        'query': 'Encceja OR "Exame Nacional * Certificação * Competências * Jovens * Adultos" OR "Certificação * Competências * Jovens * Adultos"',
        'tags': ('Educação Básica', 'Encceja'),
        'priority': 40,
    },{
        'query': 'Educacenso OR "Censo Escolar * Educação Básica"',
        'tags': ('Educação Básica', 'Educacenso'),
        'priority': 40,
    },{
        'query': 'Revalida OR "Exame Nacional * Revalidação * Diplomas Médicos"',
        'tags': ('Educação Superior', 'Revalida'),
        'priority': 40,
    },{
        'query': 'AnaSEM OR "Avaliação Nacional Seriada * Estudantes * Medicina"',
        'tags': ('Educação Superior', 'AnaSEM'),
        'priority': 40,
    },{
        'query': 'ENADE OR "Exame Nacional * Desempenho * Estudantes"',
        'tags': ('Educação Superior', 'ENADE'),
        'priority': 30,
    },{
        'query': 'Sinaes OR "Sistema Nacional * Avaliação * Educação Superior"',
        'tags': ('Educação Superior', 'Sinaes'),
        'priority': 30,
    },{
        'query': 'BASIs OR "Banco * Avaliadores * Sistema Nacional * Avaliação * Educação Superior" IR "Banco * Avaliadores"',
        'tags': ('Educação Superior', 'BASIs'),
        'priority': 30,
    },{
        'query': '"Avaliação * Curso* * Graduação"',
        'tags': ('Educação Superior', 'Termo', 'Avaliação * Curso* * Graduação'),
        'priority': 30,
    },{
        'query': '"Censo * Educação Superior"',
        'tags': ('Educação Superior', 'Censo * Educação Superior'),
        'priority': 30,
    },{
        'query': 'Inep OR "Instituto Nacional * Estudos * Pesquisas Educacionais Anísio Teixeira"',
        'tags': ('Institucional', 'Organização', 'Inep'),
        'priority': 20,
    },{
        'query': 'Cibec OR "Centro * Informação * Biblioteca * Educação"',
        'tags': ('Institucional', 'Organização', 'Cibec'),
        'priority': 20,
    },{
        'query': '"Maria Inês Fini"',
        'tags': ('Institucional', 'Pessoa', "Maria Inês Fini"),
        'priority': 20,
    },{
        'query': '"Luana Bergmann Soares"',
        'tags': ('Institucional', 'Pessoa', 'Luana Bergmann Soares'),
        'priority': 20,
    },{
        'query': '"Carlos Eduardo Moreno Sampaio"',
        'tags': ('Institucional', 'Pessoa', 'Carlos Eduardo Moreno Sampaio'),
        'priority': 25,
    },{
        'query': '"Eunice de Oliveira Ferreira Santos"',
        'tags': ('Institucional', 'Pessoa', 'Eunice de Oliveira Ferreira Santos'),
        'priority': 25,
    },{
        'query': '"Valdir QuintAna Gomes Junior"',
        'tags': ('Institucional', 'Pessoa', 'Valdir QuintAna Gomes Junior'),
        'priority': 25,
    },{
        'query': '"Camilo Mussi"',
        'tags': ('Institucional', 'Pessoa', '"Camilo Mussi"'),
        'priority': 25,
    },{
        'query': 'Rui Barbosa Brito Júnior',
        'tags': ('Institucional', 'Pessoa', 'Rui Barbosa Brito Júnior'),
        'priority': 20,
    },{
        'query': '"Avaliações Educacionais"',
        'tags': ('Termo', 'Avaliações Educacionais'),
        'priority': 10,
    },{
        'query': '"Avaliação Educacional"',
        'tags': ('Termo', 'Avaliação Educacional'),
        'priority': 10,
    })
}]


class Command(ScrapyCommand):

    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs a list of spiders or all with args'
        
    def run(self, args, opts):
        # FIXME add path from args
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
                    date_time = cron_iter.get_next(datetime).utctimetuple()
                    day_of_week = 7 if date_time.tm_wday == 0 else str(date_time.tm_wday)
                    
                    for keyword in job['search_arg_keywords']:
                        periodic_job = {
                            'description': '',
                            'addtags': keyword['tags'],
                            'minutes_shift': str(minutes),
                            # FIXME use corrected way of timezone
                            'hour': str(date_time.tm_hour+3),
                            'day': '*' if days_of_week == '*' else str(day_of_week),
                            'dayofmonth': '*' if days == '*' else str(date_time.tm_mday),
                            'month': '*' if months == '*' else str(date_time.tm_mon),
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