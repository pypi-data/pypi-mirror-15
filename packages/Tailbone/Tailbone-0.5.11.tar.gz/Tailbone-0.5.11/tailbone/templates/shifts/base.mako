## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />

<%def name="head_tags()">
    ${parent.head_tags()}
    ${h.stylesheet_link(request.static_url('tailbone:static/css/timesheet.css'))}
    <script type="text/javascript">

      $(function() {

          $('.timesheet-header select').selectmenu();

          $('.week-picker #date').datepicker({
              dateFormat: 'yy-mm-dd',
              changeYear: true,
              changeMonth: true,
              showButtonPanel: true,
              onSelect: function(dateText, inst) {
                  $(this).focus().select();
              }
          });

          $('.week-picker form').submit(function() {
              location.href = '?date=' + $('.week-picker #date').val();
              return false;
          });

      });

    </script>
</%def>

<%def name="timesheet(employees, employee_column=True)">
    <style type="text/css">
      .timesheet thead th {
          width: ${'{:0.2f}'.format(100.0 / float(9 if employee_column else 8))}%;
      }
    </style>
    <div class="timesheet-header">

##       <div class="field-wrapper employee">
##         <label>Employee</label>
##         <div class="field">
##           ${employee}
##         </div>
##       </div>

      <div class="fieldset">

        <div class="field-wrapper week">
          <label>Store</label>
          <div class="field">
            ${form.select('store', store_options, selected_value=store.uuid if store else None)}
          </div>
        </div>

        <div class="field-wrapper week">
          <label>Department</label>
          <div class="field">
            ${form.select('department', department_options, selected_value=department.uuid if department else None)}
          </div>
        </div>

        <div class="field-wrapper week">
          <label>Week of</label>
          <div class="field">
            ${week_of}
          </div>
        </div>

      </div>

      <div class="week-picker">
        ${h.form(request.current_route_url())}
        ${h.link_to(u"« Previous", '?date=' + prev_sunday.strftime('%Y-%m-%d'), class_='button')}
        ${h.link_to(u"Next »", '?date=' + next_sunday.strftime('%Y-%m-%d'), class_='button')}
        <label>Jump to week:</label>
        ${h.text('date', value=sunday.strftime('%Y-%m-%d'))}
        ${h.submit('go', "Go")}
        ${h.end_form()}
      </div>

    </div><!-- timesheet-header -->

    <table class="timesheet">
      <thead>
        <tr>
          % if employee_column:
              <th>Employee</th>
          % endif
          % for day in weekdays:
              <th>${day.strftime('%A')}<br />${day.strftime('%b %d')}</th>
          % endfor
          <th>Total<br />Hours</th>
        </tr>
      </thead>
      <tbody>
        % for employee in sorted(employees, key=unicode):
            <tr>
              % if employee_column:
                  <td class="employee">${employee}</td>
              % endif
              % for day in employee.weekdays:
                  <td>
                    % for shift in day['shifts']:
                        <p class="shift">${shift.get_display(request.rattail_config)}</p>
                    % endfor
                  </td>
              % endfor
              <td>${employee.hours_display}</td>
            </tr>
        % endfor
        % if employee_column:
            <tr class="total">
              <td class="employee">${len(employees)} employees</td>
              % for day in weekdays:
                  <td></td>
              % endfor
              <td></td>
            </tr>
        % else:
            <tr>
              % for day in employee.weekdays:
                  <td>${day['hours_display']}</td>
              % endfor
              <td>${employee.hours_display}</td>
            </tr>
        % endif
      </tbody>
    </table>
</%def>
