## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />

<%def name="head_tags()">
    ${parent.head_tags()}
    ${h.stylesheet_link(request.static_url('tailbone:static/css/timesheet.css'))}
    <script type="text/javascript">

      $(function() {

          $('.timesheet-wrapper form').submit(function() {
              $('.timesheet-header').mask("Fetching data");
          });

          $('.timesheet-header select').selectmenu({
              change: function(event, ui) {
                  $(ui.item.element).parents('form').submit();
              }
          });

          $('.timesheet-header a.goto').click(function() {
              $('.timesheet-header').mask("Fetching data");
          });

          $('.week-picker button.nav').click(function() {
              $('.week-picker #date').val($(this).data('date'));
          });

          $('.week-picker #date').datepicker({
              dateFormat: 'mm/dd/yy',
              changeYear: true,
              changeMonth: true,
              showButtonPanel: true,
              onSelect: function(dateText, inst) {
                  $(this).parents('form').submit();
              }
          });

      });

    </script>
</%def>

<%def name="context_menu()"></%def>

<%def name="timesheet(employee_column=True)">
    <style type="text/css">
      .timesheet thead th {
          width: ${'{:0.2f}'.format(100.0 / float(9 if employee_column else 8))}%;
      }
    </style>

    <div class="timesheet-wrapper">

      ${form.begin()}

      <table class="timesheet-header">
        <tbody>
          <tr>

            <td class="filters" rowspan="2">

  ##                 <div class="field-wrapper employee">
  ##                   <label>Employee</label>
  ##                   <div class="field">
  ##                     ${employee}
  ##                   </div>
  ##                 </div>

              ${form.field_div('store', h.select('store', store.uuid if store else None, store_options))}

              ${form.field_div('department', h.select('department', department.uuid if department else None,  department_options))}

              <div class="field-wrapper week">
                <label>Week of</label>
                <div class="field">
                  ${week_of}
                </div>
              </div>

            </td><!-- filters -->

            <td class="menu">
              <ul id="context-menu">
                ${self.context_menu()}
              </ul>
            </td><!-- menu -->
          </tr>

          <tr>
            <td class="tools">
              <div class="grid-tools">
                <div class="week-picker">
                  <button class="nav" data-date="${prev_sunday.strftime('%m/%d/%Y')}">&laquo; Previous</button>
                  <button class="nav" data-date="${next_sunday.strftime('%m/%d/%Y')}">Next &raquo;</button>
                  <label>Jump to week:</label>
                  ${form.text('date', value=sunday.strftime('%m/%d/%Y'))}
                </div>
              </div><!-- grid-tools -->
            </td><!-- tools -->
          </tr>

        </tbody>
      </table><!-- timesheet-header -->

      ${form.end()}

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
    </div><!-- timesheet-wrapper -->
</%def>
