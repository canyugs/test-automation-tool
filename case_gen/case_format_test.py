robot_setting = '*** Settings ***\nResource    ../setup.txt\n'
robot_variables = '*** Variables ***\n'
robot_testcases = '*** Test Cases ***\n'
robot_keywords = '*** Keywords ***\n'

case = {
    u'created_by': 2,
    u'created_on': 1447143173,
    u'custom_auto_complexity': None,
    u'custom_automated_status': 1,
    u'custom_case_note': None,
    u'custom_case_status': 3,
    u'custom_estimate': 1,
    u'custom_platform': [1, 2, 3, 4, 5, 6, 7],
    u'custom_preconds': u'KKBOX \u672a\u767b\u5165\u3002\r\n',
    u'custom_steps_separated': [
            {u'content': u'\u7528\u96fb\u5b50\u90f5\u4ef6/FB \u767b\u5165',u'expected': u'\u767b\u5165\u6210\u529f'},
            {u'content': u'\u767b\u51fa', u'expected': u'\u767b\u51fa\u6210\u529f'},
            {u'content': u'\u7528\u6b65\u9a5f 1 \u76f8\u540c\u7684\u65b9\u5f0f\u518d\u767b\u5165\u4e00\u6b21',u'expected': u'\u767b\u5165\u6210\u529f'}],
    u'estimate': None,
    u'estimate_forecast': None,
    u'id': 1234,
    u'milestone_id': None,
    u'priority_id': 2,
    u'refs': None,
    u'section_id': 320,
    u'suite_id': 29,
    u'title': u'\u540c\u4e00\u500b\u5e33\u865f\u53ef\u4ee5\u91cd\u8907\u767b\u5165/\u767b\u51fa',
    u'type_id': 6,
    u'updated_by': 2,
    u'updated_on': 1449564379}

setting = robot_setting
title = robot_testcases + case['title']
tag = {
        'doc': '    [Documentation]',
        'setup': '    [Setup]',
        'tags': '    [Tags]'}

#  TODO If there are precondition displayed, add '[setup]    Preconditions'
#       and Keywords Preconditions
#  TODO Check content and expect inside have '\n' or not
#  TODO detect 'for xxx', if is showing not write in case

steps = ""
for num in range(len(case[u'custom_steps_separated'])):
    steps += ('    ' + case[u'custom_steps_separated'][num][u'content'] + ', ' + case[u'custom_steps_separated'][num][u'expected'] + '\n')

keywords = robot_keywords + ""
for num in range(len(case[u'custom_steps_separated'])):
    keywords += (case[u'custom_steps_separated'][num][u'content'] + ', ' + case[u'custom_steps_separated'][num][u'expected'] + '\n')


final = setting +'\n' + title + steps + '\n' + keywords
print final
