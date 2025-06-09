

1. Initialize the Streamlit App:

   * Set the page title to “Free AI Logo Generator” and add a robot icon.
   * Display a main heading and a short description for the app
2. Collect User Inputs:

   * Create a text input field labeled “Enter a description for your logo”.

     * Example: *“minimal robot head with neural pattern”*
   * Create another optional text input for specifying a color palette.

     * Example: *“blue, white, black”*

3. API Key Setup:

   * Define the API key (used to access the image generation service).

4. Generate Logo Button:

   * When the **“Generate Logo”** button is clicked *and* a prompt is provided:

     * Show a spinner with the message “Generating logo...”.

5. **Build Prompt for API Request:**

   * Construct a **full prompt** by combining:

     * The user’s prompt.
     * Extra fixed descriptors like “logo, minimal, modern, vector-style”.
     * Append the color palette (if provided).
   * Example full prompt: *"minimal robot head with neural pattern, logo, minimal, modern, vector-style, colors: blue, white, black"*

6. Prepare the API Request:

   * Create a `payload` dictionary with:

     * `key`: the API key.
     * `prompt`: the full prompt.
     * `negative_prompt`: discourage things like text, watermarks, or blurriness.
     * Image parameters: width, height, number of samples, inference steps, guidance scale.

7. Send API Request

   * Make a POST request to the image generation endpoint.
   * If there's an error (e.g., bad response), show an error message.

8. Handle API Response:

     If the response contains an `output` with an image URL:

     * Fetch the image from the URL.
     * Load it as a PIL image.
     * Display the image on the Streamlit app with a caption.
     * Provide a **download button** so users can save the image (`ai_logo.png`).

9. Error Handling:

     If the API fails or doesn’t return the expected data:

     Show an error message in the app.
