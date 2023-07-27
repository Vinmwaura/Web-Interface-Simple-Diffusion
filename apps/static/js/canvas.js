/* Creates a simple canvas to be used for doodles (For model conditional) */
function create_canvas(
        canvas_id,
        stroke_line_width=10,
        stoke_style="black") {
    console.log("Initializing Canvas!")

    // Canvas functionality.
    var canvas = document.getElementById(canvas_id);
    var context = canvas.getContext("2d");
    var boundings = canvas.getBoundingClientRect();

    // Handle Mouse Coordinates.
    function setMouseCoordinates(event) {
        mouseX = event.clientX - boundings.left;
        mouseY = event.clientY - boundings.top;
    }

    // Specifications.
    var mouseX = 0;
    var mouseY = 0;
    context.strokeStyle = stoke_style; // Fixed Brush colour.
    context.lineWidth = stroke_line_width; // Fixed Brush width.

    var isDrawing = false;

    // Mouse Down Event.
    canvas.addEventListener('mousedown', function(event) {
        setMouseCoordinates(event);
        isDrawing = true;

        // Start Drawing
        context.beginPath();
        context.moveTo(mouseX, mouseY);
    });

    // Mouse Move Event.
    canvas.addEventListener('mousemove', function(event) {
        setMouseCoordinates(event);

        if(isDrawing) {
            context.lineTo(mouseX, mouseY);
            context.stroke();
        }
    });

    // Mouse Up Event.
    canvas.addEventListener('mouseup', function(event) {
        setMouseCoordinates(event);
        isDrawing = false;
    });

    // Mouse Out Event.
    canvas.addEventListener ("mouseout", function(event) {
        setMouseCoordinates(event);
        isDrawing = false;
    });

    return [canvas, context];
}

function set_clear_canvas_btn(clear_btn_id, canvas, context) {
    // Handle Clear Button.
    var clearButton = document.getElementById(clear_btn_id);

    clearButton.addEventListener('click', function() {
        context.clearRect(0, 0, canvas.width, canvas.height);
    });
}
