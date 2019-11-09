# -*- coding: utf-8 -*-
import re
from django.db.models import Case, When
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from project.courses.models import TreeItem
from project.executors.models import Code, CodeTest
from project.sources.models import Source
from project.tasks.models import Source as TasksSourse
from project.langs.models import Lang
from project.tasks.models import Task

from project.training.models import Course, Topic, Content

UserModel = get_user_model()

code_tag_pattern = re.compile(r'<p>[&nbsp;]*#code[0-9]+#[&nbsp;]*</p>|[&nbsp;]*#code[0-9]+#[&nbsp;]*')
id_code_pattern = re.compile(r'[0-9]+')
html_tag_pattern = re.compile(r'</*\w+>')
html_trash_pattern = re.compile(r' style="[^"]*"')


class Command(BaseCommand):

    """ Мигрировать курсы (единовременная процедура)"""

    def create_sources(self):
        for source in Source.objects.all():
            TasksSourse.objects.create(title=source.name)

    def create_langs(self):
        Lang.objects.create(provider=Lang.PYTHON)
        Lang.objects.create(provider=Lang.CPP)
        Lang.objects.create(provider=Lang.CSHARP)

    def create_courses(self):
        for course in TreeItem.objects.filter(type=TreeItem.COURSE):
            Course.objects.create(
                order_key=course.tree_id,
                show=course.show,
                title=course.title,
                slug=course.slug,
                last_modified=course.last_modified,
                about=course.about,
                content=course.content,
                author=course.author,
                lang=Lang.objects.get(provider=Lang.PYTHON)
            )

    def create_topic(self, theme, course):
        topic = Topic.objects.create(
            show=theme.show,
            title=theme.title,
            slug=theme.slug,
            author=theme.author,
            course=course,
            last_modified=theme.last_modified
        )
        # Создаем контент
        text_nodes = re.sub(html_trash_pattern, '', theme.content)
        text_nodes = text_nodes.replace('&nbsp;', ' ')
        text_nodes = re.split(code_tag_pattern, text_nodes)

        raw_code_tags = re.findall(code_tag_pattern, theme.content)
        code_ids = list()
        nodes = []
        for tag in raw_code_tags:
            code_tag = re.sub(html_tag_pattern, "", tag)
            code_id = int(re.search(id_code_pattern, code_tag).group(0))
            code_ids.append(code_id)

        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(code_ids)])
        code_nodes = list(Code.objects.filter(id__in=code_ids).order_by(preserved))

        text_nodes.reverse()
        code_nodes.reverse()
        while len(text_nodes) or len(code_nodes):

            if len(text_nodes):
                text = text_nodes.pop()
                if re.sub(html_tag_pattern, '', text).strip() != '':
                    nodes.append(text)
            if len(code_nodes):
                nodes.append(code_nodes.pop())

        for node in nodes:
            if isinstance(node, str):
                ct = Content.objects.create(
                    text=node,
                    type=Content.TEXT,
                    topic=topic
                )
            else:
                ct = Content.objects.create(
                    input=node.input,
                    content=node.content,
                    type=Content.ACE,
                    show_input=node.show_input,
                    topic=topic
                )

    def create_topics(self):
        # Python
        python = TreeItem.objects.get(id=5)
        python_themes = TreeItem.objects.filter(type=TreeItem.THEME, parent=python)
        python_course = Course.objects.get(slug='python')
        for theme in python_themes:
            self.create_topic(theme, python_course)

        # C++
        cpp = TreeItem.objects.get(id=1355)
        cpp_themes = TreeItem.objects.filter(type=TreeItem.THEME, parent=cpp)
        cpp_course = Course.objects.get(slug='cplusplus')
        for theme in cpp_themes:
            self.create_theme(theme, cpp_course)

        # C#
        csharp = TreeItem.objects.get(id=1356)
        csharp_themes = TreeItem.objects.filter(type=TreeItem.THEME, parent=csharp)
        csharp_course = Course.objects.get(slug='csharp')
        for theme in csharp_themes:
            self.create_theme(theme, csharp_course)

    def create_tasks(self):
        for treeitem in TreeItem.objects.filter(type=TreeItem.TASK):
            code = Code.objects.filter(treeitem=treeitem).first()
            tests = []
            if code is not None:
                tests = [{'input': test.input, 'output': test.output} for test in CodeTest.objects.filter(code=code)]
            text_nodes = re.sub(html_trash_pattern, '', treeitem.content)
            text_nodes = text_nodes.replace('&nbsp;', ' ')
            content = re.split(code_tag_pattern, text_nodes)[0]

            source = None
            if treeitem.source:
                source = TasksSourse.objects.get(title=treeitem.source.name)

            Task.objects.create(
                show=treeitem.show,
                last_modified=treeitem.last_modified,
                title=treeitem.title,
                author=treeitem.author,
                content=content,
                source=source,
                source_raw_id=treeitem.source_raw_id,
                tests=tests
            )


    def handle(self, *args, **options):

        # self.create_sources()
        # self.create_langs()
        # self.create_courses()
        # self.create_topics()
        self.create_tasks()