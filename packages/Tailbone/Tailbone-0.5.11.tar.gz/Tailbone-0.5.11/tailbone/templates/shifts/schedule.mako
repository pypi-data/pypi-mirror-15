## -*- coding: utf-8 -*-
<%inherit file="/shifts/base.mako" />

<%def name="title()">Schedule: ${sunday}</%def>

<ul id="context-menu">
  <li>${h.link_to("Print this Schedule", '#')}</li>
  <li>${h.link_to("Edit this Schedule", '#')}</li>
</ul>

${self.timesheet(employees)}
