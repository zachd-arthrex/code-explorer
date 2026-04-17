import re

with open(r'C:\Users\ZDominguez\code-explorer\public\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the sidebar section (target-tabs through queue-area + actions)
old_sidebar = '''      <div class="sidebar-section">
        <div id="target-tabs" class="target-tabs" style="display:none">
          <button class="target-tab active" data-target="program">Program</button>
          <button class="target-tab tab-fn-a" data-target="a">Fn A</button>
          <button class="target-tab tab-fn-b" data-target="b">Fn B</button>
        </div>
        <div class="sidebar-label" id="cmd-label">Commands</div>'''

new_sidebar = '''      <div class="sidebar-section">
        <div class="sidebar-label" id="cmd-label">Commands</div>'''

assert old_sidebar in content, "Could not find old sidebar"
content = content.replace(old_sidebar, new_sidebar)

# 2. Replace call-section + fn-previews + "My Program" label + queue-area + actions
old_fn = '''        <div id="call-section" style="display:none">
          <div class="call-btns">
            <button class="call-btn call-a" id="call-a-main">Call A</button>
            <button class="call-btn call-b" id="call-b-main">Call B</button>
          </div>
        </div>
      </div>

      <div id="fn-previews" class="fn-previews" style="display:none">
        <div class="fn-preview fn-a" id="fn-preview-a">
          <div class="fn-preview-header">
            <span class="fn-preview-label">Fn A:</span>
            <span class="fn-preview-steps" id="fn-a-preview-steps"><em class="fn-empty">empty</em></span>
            <button class="fn-clear-btn" data-fn="a">Clear</button>
          </div>
        </div>
        <div class="fn-preview fn-b" id="fn-preview-b">
          <div class="fn-preview-header">
            <span class="fn-preview-label">Fn B:</span>
            <span class="fn-preview-steps" id="fn-b-preview-steps"><em class="fn-empty">empty</em></span>
            <button class="fn-clear-btn" data-fn="b">Clear</button>
          </div>
        </div>
      </div>

      <div class="sidebar-label" style="padding:8px 10px 0;">My Program</div>
      <div class="queue-area" id="queue-area"></div>

      <div class="queue-actions">
        <button class="btn-clear" id="btn-clear">Clear</button>
        <button class="btn-run" id="btn-run">\u25b6 Run</button>
      </div>'''

new_fn = '''        <div id="fn-call-btns" class="fn-call-btns" style="display:none"></div>
      </div>

      <div class="lists-area" id="lists-area">
        <div class="list-panel list-panel-active" id="panel-program" data-target="program">
          <div class="list-header list-header-program" data-target="program">
            <span>\u25b6 My Program</span>
          </div>
          <div class="queue-area" id="queue-area"></div>
        </div>
        <div id="fn-panels-area"></div>
        <div id="add-fn-row" style="display:none; padding: 4px 8px;">
          <button class="add-fn-btn" id="btn-add-fn">+ Add Function</button>
        </div>
      </div>

      <div class="queue-actions">
        <button class="btn-clear" id="btn-clear">Clear</button>
        <button class="btn-run" id="btn-run">\u25b6 Run</button>
      </div>'''

assert old_fn in content, "Could not find old fn section"
content = content.replace(old_fn, new_fn)

with open(r'C:\Users\ZDominguez\code-explorer\public\index.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("HTML replacement OK")
