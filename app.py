import gradio as gr

def parse_input(text):
    text = text.replace(" ", "")
    parts = text.split(",")
    try:
        return [int(p) for p in parts if p != ""]
    except ValueError:
        return []

def bubble_sort_states(arr):
    arr = arr.copy()
    states = []
    n = len(arr)
    states.append(arr.copy())
    while True:
        swapped = False
        for i in range(0, n - 1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
                states.append(arr.copy())
        if not swapped:
            break
    return states

def rank_to_hsl(rank, total):
    if total <= 1:
        hue = 200
    else:
        hue = int((rank / max(1, (total - 1))) * 280)
    return f"hsl({hue}, 85%, 65%)", f"hsl({hue}, 75%, 50%)"

def format_state_html(state, is_sorted=False):
    wrapper_class = " sorted" if bool(is_sorted) else ""
    html = '<div class="vis-wrap{}">'.format(wrapper_class)
    
    if bool(is_sorted):
        html += '<div class="sorted-banner">✓ Sorted!</div>'
    
    html += '<div class="boxes">'

    if len(state) > 0:
        mx = max(state)
        mn = min(state)
    else:
        mx = 1
        mn = 0

    sorted_vals = sorted(state)
    positions = {}
    for i, v in enumerate(sorted_vals):
        positions.setdefault(v, []).append(i)

    total = len(state)
    for x in state:
        height = 90
        if mx != mn:
            height = 90 + int((x - mn) / (mx - mn) * 180)

        rank_for_color = 0
        if positions.get(x):
            rank_for_color = positions[x].pop(0)
        bg, border = rank_to_hsl(rank_for_color, total)

        box_html = (
            f'<div class="box" style="height:{height}px; '
            f'background:linear-gradient(135deg, {bg} 0%, {border} 100%); '
            f'border:2px solid {border}; '
            f'box-shadow: 0 4px 15px rgba(0,0,0,0.15), inset 0 1px 3px rgba(255,255,255,0.3);">'
            f'<div class="num">{x}</div>'
            f'</div>'
        )
        html += str(box_html)

    html += '</div></div>'
    return html

def init_states(text):
    arr = parse_input(text)
    states = bubble_sort_states(arr)
    if not states:
        first_html = '<div class="empty-state">🔢 Enter comma-separated numbers to begin</div>'
        return first_html, [], 0, gr.update(interactive=False), gr.update()
    first_html = format_state_html(states[0], is_sorted=(len(states) == 1))
    
    # Enable button only if there are more steps
    button_update = gr.update(interactive=(len(states) > 1))
    
    # Keep button as "Start" when initializing
    return first_html, states, 0, button_update, gr.update()

def next_step(states, current_step):
    if not states:
        return '<div class="empty-state">🔢 Enter comma-separated numbers to begin</div>', 0, gr.update(), gr.update()
    if current_step < len(states) - 1:
        current_step += 1
    is_sorted = (current_step == len(states) - 1)
    
    # Disable button if we're at the last step
    button_update = gr.update(interactive=(current_step < len(states) - 1))
    
    # Change start button to Reset after first step
    start_btn_update = gr.update(value="🔄 Reset")
    
    return format_state_html(states[current_step], is_sorted), current_step, button_update, start_btn_update

# ---------- UI ----------
with gr.Blocks() as demo:
    
    # Inline CSS
    gr.HTML("""
    <style>
    /* Global Styles */
    .gradio-container {
        max-width: 1100px !important;
        margin: 0 auto !important;
        padding: 40px 20px !important;
    }
    
    /* Header Styles */
    .header {
        text-align: center;
        margin-bottom: 40px;
        padding-bottom: 30px;
        border-bottom: 3px solid #f0f0f0;
    }
    
    .title {
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 12px;
        letter-spacing: -1px;
    }
    
    .subtitle {
        font-size: 18px;
        color: #666;
        line-height: 1.6;
        max-width: 700px;
        margin: 0 auto;
    }
    
    /* Input Section */
    .input-section {
        background: #f8f9fa;
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 30px;
        border: 2px solid #e9ecef;
    }
    
    label {
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #333 !important;
        margin-bottom: 12px !important;
    }
    
    input[type="text"], textarea {
        background-color: white !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-size: 18px !important;
        color: #333 !important;
        transition: all 0.3s ease !important;
    }
    
    input[type="text"]:focus, textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    /* Visualization Area */
    .vis-wrap {
        margin: 30px 0;
        position: relative;
        min-height: 320px;
        background: linear-gradient(to bottom, #f8f9fa 0%, #ffffff 100%);
        border-radius: 16px;
        padding: 40px 20px;
        border: 2px solid #e9ecef;
    }
    
    .vis-wrap.sorted {
        background: linear-gradient(135deg, #fff5f5 0%, #ffe5e5 100%);
        border-color: #ff6b6b;
        animation: sortedPulse 1s ease;
    }
    
    @keyframes sortedPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .sorted-banner {
        position: absolute;
        right: 20px;
        top: 20px;
        background: linear-gradient(135deg, #51cf66 0%, #37b24d 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 16px;
        box-shadow: 0 4px 20px rgba(55, 178, 77, 0.4);
        animation: bounceIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0) rotate(-180deg); opacity: 0; }
        50% { transform: scale(1.1) rotate(10deg); }
        100% { transform: scale(1) rotate(0deg); opacity: 1; }
    }
    
    .boxes {
        display: flex;
        gap: 16px;
        align-items: flex-end;
        justify-content: center;
        padding: 20px;
        transition: all 0.5s ease;
        flex-wrap: wrap;
    }
    
    .box {
        width: 85px;
        min-width: 50px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        cursor: pointer;
    }
    
    .box:hover {
        transform: translateY(-12px) scale(1.05);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25) !important;
        filter: brightness(1.1);
    }
    
    .num {
        font-weight: 800;
        font-size: 22px;
        color: white;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        padding: 10px;
        background: rgba(0, 0, 0, 0.15);
        border-radius: 10px;
        backdrop-filter: blur(5px);
    }
    
    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: #999;
        font-size: 20px;
        font-weight: 500;
    }
    
    /* Buttons */
    .btn-row {
        display: flex;
        gap: 16px;
        margin: 30px 0;
    }
    
    button.primary-btn {
        flex: 1;
        padding: 18px 32px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        border: none !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    button.primary-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5) !important;
    }
    
    button.secondary-btn {
        flex: 1;
        padding: 18px 32px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        border: none !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4) !important;
    }
    
    button.secondary-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(245, 87, 108, 0.5) !important;
    }
    
    button.secondary-btn:disabled {
        background: #cccccc !important;
        color: #666666 !important;
        box-shadow: none !important;
        cursor: not-allowed !important;
        opacity: 0.6;
    }
    
    button.secondary-btn:disabled:hover {
        transform: none;
        box-shadow: none !important;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 20px 30px;
        border-radius: 12px;
        text-align: center;
        color: #000000 !important;
        font-size: 15px;
        line-height: 1.6;
        border: 2px solid #90caf9;
        margin-top: 30px;
    }
    
    .info-box strong {
        color: #000000 !important;
    }
    
    .info-box * {
        color: #000000 !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .title { font-size: 36px; }
        .subtitle { font-size: 16px; }
        .box { width: 65px; min-width: 45px; }
        .num { font-size: 18px; }
        button.primary-btn, button.secondary-btn { font-size: 16px !important; padding: 14px 24px !important; }
    }
    </style>
    """)

    # Header
    gr.HTML("""
        <div class='header'>
            <div class='title'>🎨 Bubble Sort Visualizer</div>
            <div class='subtitle'>
                Step through the bubble sort algorithm and watch elements swap positions in real-time. 
                Each bar's color represents its final sorted position—smallest values are red, largest are purple. 
                Click "Next Step" to see each comparison and swap until the array forms a rainbow from left to right.
            </div>
        </div>
    """)

    # Input Section
    with gr.Group():
        input_box = gr.Textbox(
            label="📝 Enter Your Numbers",
            lines=1,
            max_lines=1,
            placeholder="Try: 8, 3, 15, 1, 12, 6, 20, 4",
        )

    # Visualization Display
    state_display = gr.HTML('<div class="empty-state">🔢 Enter comma-separated numbers to begin</div>')

    # State Management
    states_state = gr.State([])
    step_state = gr.State(0)

    # Control Buttons
    with gr.Row():
        start_btn = gr.Button("🚀 Start", elem_classes="primary-btn")
        next_btn = gr.Button("➡️ Next Step", elem_classes="secondary-btn")

    # Info Box
    gr.HTML("""
        <div class='info-box'>
            💡 <strong>How it works:</strong> Bubble sort compares adjacent elements and swaps them if they're out of order. 
            Each pass moves the largest unsorted value to its correct position (like a bubble rising). 
            <strong>Time complexity:</strong> O(n²) worst case, O(n) best case (already sorted). 
            <strong>Space:</strong> O(1) – sorts in place. Not practical for large datasets, but great for learning!
        </div>
    """)

    # Event Handlers
    start_btn.click(
        fn=init_states,
        inputs=input_box,
        outputs=[state_display, states_state, step_state, next_btn, start_btn],
    )

    next_btn.click(
        fn=next_step,
        inputs=[states_state, step_state],
        outputs=[state_display, step_state, next_btn, start_btn],
    )

if __name__ == "__main__":
    demo.launch()