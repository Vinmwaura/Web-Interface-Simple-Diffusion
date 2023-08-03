/* Creates a simple canvas to be used for doodles (For model conditional) */
function create_canvas(
        canvas_id,
        clear_btn_id,
        image_url,
        stroke_line_width=20,
        stoke_style="black",
        linecap="round",
        linejoin="round") {
    console.log("Initializing Canvas!")

    // Canvas functionality.
    var canvas = document.getElementById(canvas_id);
    var context = canvas.getContext("2d");
    
    // Background Image in cavas
    var background;
    if (image_url) {
        background = new Image();
        background.src = image_url;

        // Make sure the image is loaded first otherwise nothing will draw.
        background.onload = function(){
            context.drawImage(background, 0, 0);   
        }
    }

    // Handles Clearing of the Canvas.
    var clearButton = document.getElementById(clear_btn_id);

    clearButton.addEventListener('click', function() {
        context.clearRect(0, 0, canvas.width, canvas.height);

        if(background) {
            // Reload background Image into canvas.
            context.drawImage(background, 0, 0);
        }
    });

    // Handle Mouse Coordinates.
    function setMouseCoordinates(event) {
        // boundings = Mouse click event.
        boundings = event.target.getBoundingClientRect();
        
        mouseX = event.clientX - boundings.left; //x position within the element.
        mouseY = event.clientY - boundings.top;  //y position within the element.
    }

    // Specifications.
    var mouseX = 0;
    var mouseY = 0;

    context.strokeStyle = stoke_style; // Fixed Brush colour.
    context.lineWidth = stroke_line_width; // Fixed Brush width.
    context.lineCap = linecap; // End caps for a line (Brush type).
    context.lineJoin = linejoin; // Sets or returns the type of corner created, when two lines meet.

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

        if (isDrawing) {
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

    return [canvas, context, background];
}
