# Bubble Sort Visualizer

## Demo video/gif/screenshot of test



https://github.com/user-attachments/assets/4b7f019f-d1cb-44ca-b2bf-3938a255c69f



## Problem Breakdown & Computational Thinking (You can add a flowchart and write the four pillars of computational thinking briefly in bullets)

### Decomposition

-  **Input Parsing:** Convert the user's comma-separated string into a list of integers
  
-  **State Generation:** Generate all intermediate array states during sorting
  
-  **Comparison Phase:** Compare adjacent elements (arr[i] vs arr[i+1])
  
-  **Swap Operation:** Swap elements if they're out of order
  
-  **Pass Completion:** Complete one full pass through the array
  
-  **Termination Check:** Stop when no swaps occur in a complete pass
  
-  **Visualization Rendering:** Convert each array state into HTML bars with colors

### Pattern Recognition

-  **Nested Iteration**: Outer loop for passes, inner loop for comparisons
  
-  **Adjacent Comparison:** Always comparing pairs (i, i+1)
  
-  **Conditional Swap:** If arr[i] > arr[i+1], swap them
  
-  **State Capture:** After each swap, save the current array state
  
-  **Color Assignment:** Each value gets a color based on its sorted rank (red→purple gradient)

### Abstraction – What to Show vs. Hide
#### SHOWN to the user:

- Visual bars representing array values (height = magnitude)

- Color gradient showing final sorted position (red=smallest, purple=largest)

- Each intermediate state after a swap occurs

- Final "Sorted!" indicator when complete

- Step-by-step progression with "Next Step" button

- Algorithm complexity information (O(n²) time, O(1) space)

#### HIDDEN from the user:

- Loop indices (i, j counters)

- Internal comparison logic details

- Memory addresses or technical implementation

- Exact number of comparisons made

- Pass numbers or iteration counts

- HSL color calculation formulas

### Algorithm Design
#### Input:

- **Data Type:** String (comma-separated integers)

- **Structure:** Text input via Gradio textbox

- **Example:** "8, 3, 15, 1, 12, 6, 20, 4"

#### Processing:

- Parse string → integer list using parse_input()

- Generate all sorting states with bubble_sort_states()

- Store states in session state variable

- On each "Next Step" click, increment to next state

- Calculate color gradient based on sorted rank using rank_to_hsl()

- Render bars as styled HTML divs with format_state_html()

#### Output:

- **GUI Display:** Animated colored bars (HTML/CSS)

- **Interactive Controls:** "Start" and "Next Step" buttons

- **Visual Feedback:** Bars with height proportional to value, colors showing sorted position

- **Status Indicator:** Green "Sorted!" banner when complete

## Steps to Run
1. Enter a comma-separated list of numbers in the input box (for example: 5, 3, 1, 2).
2. Click "Start" to initialize the visualization.
3. Click "Next Step" to step through each comparison and swap.
4. When sorted, a "Sorted!" message will appear.
5. Reset anytime using the "Reset" button.

## Hugging Face Link

https://huggingface.co/spaces/aunzite/Bubble_Sort_Visualizer

## Author & Acknowledgment
Author: Aun Ali

## Acknowledgments:

- Gradio for the UI framework used to build the interactive visualizer

- Python Software Foundation (PSF) for the Python language and documentation

- Standard CS algorithm resources for the bubble sort concept
