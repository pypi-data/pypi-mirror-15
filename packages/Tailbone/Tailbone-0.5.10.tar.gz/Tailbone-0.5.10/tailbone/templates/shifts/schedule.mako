## -*- coding: utf-8 -*-
<%inherit file="/shifts/base.mako" />

<%def name="title()">Schedule: ${sunday}</%def>

${self.timesheet(employees)}
