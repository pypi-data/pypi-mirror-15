## -*- coding: utf-8 -*-
<%inherit file="/shifts/base.mako" />

<%def name="context_menu()">
    % if request.has_perm('timesheet.view'):
        <li>${h.link_to("View this Time Sheet", url('schedule.goto.timesheet'), class_='goto')}</li>
    % endif
##     <li>${h.link_to("Print this Schedule", '#')}</li>
##     <li>${h.link_to("Edit this Schedule", '#')}</li>
</%def>

${self.timesheet()}
