import sys
import json
import re
from datetime import datetime, timezone
from scrapy.commands import ScrapyCommand
from croniter import croniter

# -*- coding: utf-8 -*-

jobs = [{
    'schedules': (
        '0 8,12,17 * * MON,TUE,WED,THU,FRI',
        '0 12,18 * * SAT,SUN',
    ),
    # FIXME get spider name from command argument
    'spiders': ['all'],
    'search_arg_keywords': ({
        'query': 'Celpe-Bras OR "Certificado * Proficiência * Língua Portuguesa"',
        'tags': ('Ações Internacionais', 'CELPE-Bras'),
        'regex': '(?i)Celpe.{0,}Bras|Certificado.{0,}Nacional.{0,}Ensino.{0,}Mé?e?dio',
    },{
        'query': 'Pisa OR "Programme * International Student Assessment"',
        'tags': ('Ações Internacionais', 'Pisa'),
        'regex': '(?i)Pisa|Programme.{0,}International.{0,}Student.{0,}Assessment',
    },{
        'query': 'EAG OR "Education * Glance"',
        'tags': ('Ações Internacionais', 'EAG'),
        'regex': '(?i)EAG|Education.{0,}Glance',
    },{
        'query': 'TALIS OR "Pesquisa Internacional sobre Ensino * Aprendizagem" OR "Teaching * Learning International Survey"',
        'tags': ('Ações Internacionais', 'TALIS'),
        'regex': '(?i)TALIS|Pesquisa.{0,}Internacional.{0,}sobre.{0,}Ensino.{0,}Aprendizagem|Teaching.{0,}Learning.{0,}International.{0,}Survey',
    },{
        'query': 'Enem OR "Exame Nacional * Ensino Médio"',
        'tags': ('Educação Básica', 'Enem'),
        'regex': '(?i)Enem|Exame.{0,}Nacional.{0,}Ensino.{0,}Mé?e?dio',
    },{
        'query': '"Prova Brasil" OR "Avaliação Nacional * Rendimento Escolar"',
        'tags': ('Educação Básica', 'Prova Brasil'),
        'regex': '(?i)Prova.{0,}Brasil|Avaliação.{0,}Nacional.{0,}Rendimento.{0,}Escolar',
    },{
        'query': '"Provinha Brasil"',
        'tags': ('Educação Básica', 'Provinha Brasil'),
        'regex': '(?i)Provinha.{0,}Brasil',
    },{
        'query': 'ANA OR "Avaliação Nacional * Alfabetização"',
        'tags': ('Educação Básica', 'ANA'),
        'regex': '(?i)ANA|Avaliação.{0,}Nacional.{0,}Alfabetizaç?c?ã?a?o',
    },{
        'query': 'Aneb OR "Avaliação Nacional * Educação Básica"',
        'tags': ('Educação Básica', 'Aneb'),
        'regex': '(?i)Aneb|Avaliaç?c?ã?a?o.{0,}Nacional.{0,}Educaç?c?ã?a?o.{0,}Bá?a?sica',
    },{
        'query': 'Saeb OR "Sistema Nacional * Avaliação * Educação Básica"',
        'tags': ('Educação Básica', 'Saeb'),
        'regex': '(?i)Saeb|Sistema.{0,}Nacional.{0,}Avaliaç?c?ã?a?o.{0,}Bá?a?sica',
    },{
        'query': 'Anresc OR "Avaliação Nacional * Rendimento Escolar"',
        'tags': ('Educação Básica', 'Anresc'),
        'regex': '(?i)Anresc|Avaliaç?c?ã?a?o.{0,}Nacional.{0,}Rendimento.{0,}Escola',
    },{
        'query': 'Encceja OR "Exame Nacional * Certificação * Competências * Jovens * Adultos" OR "Certificação * Competências * Jovens * Adultos"',
        'tags': ('Educação Básica', 'Encceja'),
        'regex': '(?i)Encceja|Exame.{0,}Nacional.{0,}Certificaç?c?ã?a?o.{0,}Competê?e?ncias.{0,}Jovens.{0,}Adultos|Certificaç?c?ã?ao.{0,}Competê?e?ncias.{0,}Jovens.{0,}Adultos',
    },{
        'query': 'Educacenso OR "Censo Escolar * Educação Básica"',
        'tags': ('Educação Básica', 'Educacenso'),
        'regex': '(?i)Educacenso|Censo.{0,}Escolar.{0,}Educaç?c?ã?a?o.{0,}Bá?a?sica',
    },{
        'query': 'Revalida OR "Exame Nacional * Revalidação * Diplomas Médicos"',
        'tags': ('Educação Superio', 'Revalida'),
        'regex': '(?i)Revalida|Exame.{0,}Nacional.{0,}Revalidação.{0,}Diplomas?.{0,}Mé?e?dicos?',
    },{
        'query': 'AnaSEM OR "Avaliação Nacional Seriada * Estudantes * Medicina"',
        'tags': ('Educação Superio', 'AnaSEM'),
        'regex': '(?i)AnaSEM|Avaliaç?c?ã?a?o.{0,}Nacional.{0,}Seriada.{0,}Estudantes?.{0,}Medicina',
    },{
        'query': 'ENADE OR "Exame Nacional * Desempenho * Estudantes"',
        'tags': ('Educação Superio', 'ENADE'),
        'regex': '(?i)ENADE|Exame.{0,}Nacional.{0,}Desempenho.{0,}Estudantes?',
    },{
        'query': 'Sinaes OR "Sistema Nacional * Avaliação * Educação Superior"',
        'tags': ('Educação Superio', 'Sinaes'),
        'regex': '(?i)Sinaes|Sistema.{0,}Nacional.{0,}Avaliaç?c?ã?a?o.{0,}Educaç?c?ã?a?o.{0,}Superio',
    },{
        'query': 'BASIs OR "Banco * Avaliadores * Sistema Nacional * Avaliação * Educação Superior" OR "Banco * Avaliadores"',
        'tags': ('Educação Superio', 'BASIs'),
        'regex': '(?i)BASIs|Banco.{0,}Avaliadores.{0,}Sistema.{0,}Nacional.{0,}Avaliaç?c?ã?a?o.{0,}Educaç?c?ã?a?o.{0,}Superior|Banco.{0,}Avaliadores',
    },{
        'query': '"Avaliação * Curso* * Graduação"',
        'tags': ('Educação Superio', 'Termo', 'Avaliação * Curso* * Graduação'),
        'regex': '(?i)Avaliaç?c?ã?a?o.{0,}Curso.{0,}Graduaç?c?ã?a?o',
    },{
        'query': '"Censo * Educação Superior"',
        'tags': ('Educação Superio', 'Censo * Educação Superio'),
        'regex': '(?i)Censo.{0,}Educaç?c?ã?a?o.{0,}Superio',
    },{
        'query': 'Inep OR "Instituto Nacional * Estudos * Pesquisas Educacionais Anísio Teixeira"',
        'tags': ('Institucional', 'Organização', 'Inep'),
        'regex': '(?i)Inep|Instituto.{0,}Nacional.{0,}Estudos.{0,}Pesquisas.{0,}Educacionais.{0,}Aní?i?sio.{0,}Teixeira',
    },{
        'query': 'Cibec OR "Centro * Informação * Biblioteca * Educação"',
        'tags': ('Institucional', 'Organização', 'Cibec'),
        'regex': '(?i)Cibec|Centro.{0,}Informaç?c?ã?a?o.{0,}Biblioteca.{0,}Educaç?c?ã?a?o',
    },{
        'query': '"Maria Inês Fini"',
        'tags': ('Institucional', 'Pessoa', "Maria Inês Fini"),
        'regex': '(?i)Maria.{0,}Inê?e?s.{0,}Fini',
    },{
        'query': '"Luana Bergmann Soares"',
        'tags': ('Institucional', 'Pessoa', 'Luana Bergmann Soares'),
        'regex': '(?i)Luana.{0,}Bergmann.{0,}Soares',
    },{
        'query': '"Carlos Eduardo Moreno Sampaio"',
        'tags': ('Institucional', 'Pessoa', 'Carlos Eduardo Moreno Sampaio'),
        'regex': '(?i)Carlos.{0,}Eduardo.{0,}Moreno.{0,}Sampaio',
    },{
        'query': '"Eunice de Oliveira Ferreira Santos"',
        'tags': ('Institucional', 'Pessoa', 'Eunice de Oliveira Ferreira Santos'),
        'regex': '(?i)Eunice.{0,}de.{0,}Oliveira.{0,}Ferreira.{0,}Santos',
    },{
        'query': '"Valdir QuintAna Gomes Junior"',
        'tags': ('Institucional', 'Pessoa', 'Valdir QuintAna Gomes Junio'),
        'regex': '(?i)Valdir.{0,}QuintAna.{0,}Gomes.{0,}Junio',
    },{
        'query': '"Camilo Mussi"',
        'tags': ('Institucional', 'Pessoa', '"Camilo.{0,}Mussi"'),
        'regex': '(?i)Camilo.{0,}Mussi',
    },{
        'query': 'Rui Barbosa Brito Júnio',
        'tags': ('Institucional', 'Pessoa', 'Rui Barbosa Brito Júnio'),
        'regex': '(?i)Rui.{0,}Barbosa.{0,}Brito.{0,}Júnio',
    },{
        'query': '"Avaliações Educacionais"',
        'tags': ('Termo', 'Avaliações Educacionais'),
        'regex': '(?i)Avaliaç?c?õ?o?es?.{0,}Educacionais',
    },{
        'query': '"Avaliação Educacional"',
        'tags': ('Termo', 'Avaliação Educacional'),
        'regex': '(?i)Avaliaç?c?ã?a?o.{0,}Educacional',
    })
}]


class Command(ScrapyCommand):

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return """Generate an JSON line *.jl file to schedule periodic jobs 
                  with bin/schedule_periodic_jobs.jh"""
        
    def run(self, args, opts):
        # FIXME add path from args
        jobs_file = open('./jobs.jl', mode='w+')
        
        for job in jobs:
            for keyword in job['search_arg_keywords']:
                if not re.search(keyword['regex'], keyword['query']):
                    raise ValueError('The keywork with query {query} don\'t match the REGEX {regex}'.format(
                        query=keyword['query'], regex=keyword['regex']
                    ))
            
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
                                        'regex': keyword['regex'], 
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