from shark.base import BaseObject
from shark.font_awesome import Icon
from shark.layout import multiple_div_row


class StatBox(BaseObject):
    def __init__(self, stat=None, name=None, icon=None, view_more_name=None, view_more_action=None, **kwargs):
        self.init(kwargs)
        self.stat = self.param(stat, 'Collection', 'The number or fact you want to show large')
        self.name = self.param(name, 'Collection', 'Name of the number or fact, such as "Users" or "Pageviews"')
        self.icon = self.param(icon, 'Collection', 'Large icon. Use any icon from Font Awesome at size 5')
        self.view_more_name = self.param(view_more_name, 'Collection', 'The text of the link under the stat to get more info. If you don\'t enter this it will not show.')
        self.view_more_action = self.param(view_more_action, 'Action', 'Action to perform when the view more area is clicked')

    def get_html(self, html):
        html.append('<div class="panel panel-primary">')
        html.append('    <div class="panel-heading">')
        html.append('        <div class="row">')
        html.append('            <div class="col-xs-3">')
        html.render('                ', self.icon)
        html.append('            </div>')
        html.append('            <div class="col-xs-9 text-right">')
        html.append('                <div class="{}">'.format(html.add_css_class('font-size: 40px;')))
        html.render('                    ', self.stat)
        html.append('                </div>')
        html.append('                <div>')
        html.render('                    ', self.name)
        html.append('                </div>')
        html.append('            </div>')
        html.append('        </div>')
        html.append('    </div>')
        html.append('    <a href="#">')
        html.append('        <div class="panel-footer">')
        html.append('            <span class="pull-left">')
        html.render('                ', self.view_more_name)
        html.append('            </span>')
        html.append('            <span class="pull-right"><i class="fa fa-arrow-circle-right"></i></span>')
        html.append('            <div class="clearfix"></div>')
        html.append('        </div>')
        html.append('    </a>')
        html.append('</div>')

    @classmethod
    def example(cls):
        return multiple_div_row(
            StatBox('26', 'New Comments', Icon('comments', 5), 'View Comments', '#'),
            StatBox('12', 'New Tasks', Icon('tasks', 5), 'View Tasks', '#')
        )

