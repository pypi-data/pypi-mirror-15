## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />

<%def name="title()">Time Sheet</%def>

<%def name="head_tags()">
  ${parent.head_tags()}
  <style type="text/css">
    .timesheet {
        border-bottom: 1px solid black;
        border-right: 1px solid black;
        width: 100%;
    }
    .timesheet thead th {
        width: 12.5%;
    }
    .timesheet thead th,
    .timesheet tbody td {
        border-left: 1px solid black;
        border-top: 1px solid black;
    }
    .timesheet tbody td {
        padding: 5px;
        text-align: center;
    }
    .timesheet tbody p.shift {
        display: block;
    }
  </style>
</%def>

<div class="field-wrapper employee">
  <label>Employee</label>
  <div class="field">
    ${employee}
  </div>
</div>

<div class="field-wrapper week">
  <label>Week of</label>
  <div class="field">
    ${week_of}
  </div>
</div>

<table class="timesheet">
  <thead>
    <tr>
      % for day in weekdays:
          <th>${day.strftime('%A')}<br />${day.strftime('%b %d')}</th>
      % endfor
      <th>Total<br />Hours</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      % for day in employee.weekdays:
          <td>
            % for shift in day['shifts']:
                <p class="shift">${shift.get_display(request.rattail_config)}</p>
            % endfor
          </td>
      % endfor
      <td>${employee.hours_display}</td>
    </tr>
    <tr>
      % for day in employee.weekdays:
          <td>${day['hours_display']}</td>
      % endfor
      <td>${employee.hours_display}</td>
    </tr>
  </tbody>
</table>
