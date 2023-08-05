## -*- coding: utf-8 -*-
<%inherit file="/shifts/base.mako" />

<%def name="title()">Time Sheet: ${sunday}</%def>

${self.timesheet(employees, employee_column=False)}
