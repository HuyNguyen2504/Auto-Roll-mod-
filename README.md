<h1>⚙️ Auto Mod Reroll – Usage Guide</h1>

<hr/>
<h2>🧩 What Is “The Thing”?</h2>

<p>
  <b>The Thing</b> is just a funny name I use, but technically it’s a form of
  <b>save scumming</b>.
</p>

<p>
  The idea is simple:
</p>

<ul>
  <li>You roll a mod and spend a lot of dice</li>
  <li>Your game <i>magically</i> crashes before saving</li>
  <li>You reopen the game</li>
  <li>All the dice you lost come back like nothing ever happened</li>
</ul>

<p>
  With this trick, you basically have an <b>infinite amount of dice</b> to roll mods.
</p>

<p>
  The problem?  
  Doing this <b>by hand</b> is extremely boring and time-consuming.
  If your luck is bad, it can easily take <b>hours</b> of nonstop clicking.
</p>

<p>
  To solve that problem, this program was created.
  <br/>
  <b>No more boring clicks.</b><br/>
  <b>No more wasting time.</b><br/>
  Just fully green, full Ancestral substat mods — so you can finally
  <i>go touch some grass</i> 🌱
</p>

<hr/>

<h2>🤖 How Does This Bot Work?</h2>

<p>
  When a mod is rolling, the in-game text changes from <b>“Auto Roll”</b> to <b>“Stop”</b>.
  Once the roll is finished, it changes back to <b>“Auto Roll”</b>.
</p>

<p>
  This program takes advantage of that behavior:
</p>

<ul>
  <li>
    After each roll, the bot checks whether the text is <b>“Auto Roll”</b>
  </li>
  <li>
    If it is, that means the roll is done
  </li>
  <li>
    The program then:
    <ul>
      <li>Checks the rolled substat</li>
      <li>If it’s good, locks it</li>
      <li>Saves the result</li>
      <li>Starts rolling again</li>
    </ul>
  </li>
</ul>

<p>
  This loop continues until the mod becomes <b>fully green</b>.
</p>

<p>
  The bot also monitors the <b>loading screen</b>,
  so you don’t have to worry if your game loads slower than usual —
  something regular auto-clickers cannot handle properly.
</p>

<p>
  If the program does <b>not</b> detect <b>“Auto Roll”</b> when expected,
  it will:
</p>

<ul>
  <li>Force the game to close</li>
  <li>Prevent cloud saving</li>
  <li>Restore the game state from before the roll</li>
</ul>

<p>
  Then it simply repeats the process until everything is finished.
</p>

<hr/>

<h2>⚠️ Is This Against the Game’s TOS?</h2>

<p>
  <b>Yes.</b>
</p>

<p>
  So please:
</p>

<ul>
  <li>Do <b>not</b> spread this publicly</li>
  <li>Only share it with people you <b>fully trust</b></li>
</ul>
<hr>
<h1> Step by Step Instruction
<h2>1️⃣ Download & Install Required Packages</h2>

<p>Before running the project, make sure all required dependencies are installed.</p>

<ul>
  <li>
    <b>Python packages</b><br/>
    Install all required Python libraries used in this project.
    You can use <b>ChatGPT</b> or <b>GitHub Copilot</b> to identify and install missing packages.
  </li>

  <li>
    <b>LDPlayer Emulator</b><br/>
    Download and install <b>LDPlayer</b>, then install the <b>Tower</b> game inside LDPlayer.
  </li>

  <li>
    <b>Tesseract OCR</b><br/>
    Download from:
    <a href="https://tesseract-ocr.github.io/tessdoc/Installation.html" target="_blank">
      https://tesseract-ocr.github.io/tessdoc/Installation.html
    </a><br/>
    Default installation path is usually:<br/>
    <code>C:\Program Files\Tesseract-OCR\tessdata</code>
  </li>

  <li>
    <b>Bark (iOS)</b><br/>
    On your iPhone (Android is not tested yet), download the app <b>Bark</b>.
  </li>
</ul>

<br/>

<img width="247" height="314" src="https://github.com/user-attachments/assets/c099218f-d421-4f5c-bc77-179a752c0438" />

<p>
  Open Bark and retrieve your <b>API Key</b>.<br/>
  The API URL format looks like this:
</p>

<pre>
https://api.day.app/{device_key}/{title}/{content}
</pre>

<img width="247" height="314" src="https://github.com/user-attachments/assets/64e357d1-d196-49fd-b476-d1262c1d0c2b" />

<hr/>

<h2>2️⃣ Calibration – Capture Mouse Coordinates</h2>

<h3>2.1 Open Calibration Tool</h3>

<ul>
  <li>Open <code>calibrationUI.py</code> in your IDE</li>
</ul>

<img width="899" height="635" src="https://github.com/user-attachments/assets/a47bc57a-53de-437b-8f9e-1f2a73349cbd" />

<h3>🖱️ How to Use Calibration UI</h3>

<ul>
  <li>
    <b>Create Buttons</b><br/>
    Hover your mouse over the position you want to auto-click and press <code>Ctrl + B</code>.
    This saves the click coordinate <code>(X, Y)</code>.<br/>
    ⚠️ Always rename buttons to avoid confusion later.
  </li>

  <li>
    <b>Create Regions</b><br/>
    Regions are used for OCR and state detection (e.g. checking Ancestral substats or roll completion).
    <ol>
      <li>Hover mouse to the <b>top-left</b> corner of the region you want to check → press <code>Ctrl + P</code></li>
      <li>Hover mouse to the <b>bottom-right</b> corner → press <code>Ctrl + P</code></li>
    </ol>
    Each region has 4 values: <code>(X, Y, Width, Height)</code>
  </li>
</ul>

<hr/>

<h3>2.2 LDPlayer Calibration</h3>

<ul>
  <li>Open <b>LDPlayer</b></li>
  <li>Hover mouse over the <b>Tower icon</b> → press <code>Ctrl + B</code></li>
</ul>

<img width="1920" height="1080" src="https://github.com/user-attachments/assets/958d4083-3378-49a5-a76b-05efd27dd3d6" />

<p>
  During the loading screen, clip a <b>region of the TechTree game logo</b>.
  This region is used to detect whether the game has fully loaded.
</p>

<img width="1920" height="1080" src="https://github.com/user-attachments/assets/f7ea27d0-dc72-4fc4-8801-96dd283afc3a" />

<p>
  Once inside the game:
</p>

<ul>
  <li>Create a button on the <b>Mod icon</b></li>
  <li>
    All mod slot coordinates (from <code>1_1</code> to <code>3_5</code>)
    are already pre-calculated in <code>variable.py</code>
  </li>
</ul>

<img width="1920" height="1080" src="https://github.com/user-attachments/assets/328e2118-95d6-4245-a5f4-0c6c2926fe43" />

<p>
  Select the mod you want to roll, then create buttons for:
</p>

<ul>
  <li><b>Mod Option</b></li>
  <li><b>Reroll Effect</b></li>
</ul>

<img width="1920" height="1080" src="https://github.com/user-attachments/assets/a2a0232a-32d1-464f-b849-54c38e5b7564" />

<p>
  ⚠️ This is the most time-consuming step:
</p>

<ul>
  <li>Each rectangle is a region that must be clipped using <code>Ctrl + P</code></li>
  <li>Inside each lock icon, create a button (explained later)</li>
  <li>Create a button on the <b>X</b> (discard roll)</li>
  <li>Create another button on <b>New</b> (save new substat)</li>
</ul>

<img width="1920" height="1080" src="https://github.com/user-attachments/assets/bc28f836-9158-484b-90c2-f432f6103930" />
<img width="1920" height="1080" src="https://github.com/user-attachments/assets/6f6c7f14-719f-42ae-acb1-e4408d979868" />

<p>
  After finishing, create a button for the small <b>X</b> button and double-check all coordinates.
</p>

<img width="1920" height="1080" src="https://github.com/user-attachments/assets/ed81217a-82b8-44e1-beb7-afccac6e418e" />
<img width="1920" height="1080" src="https://github.com/user-attachments/assets/a9c7a0c6-5b35-4c53-bf68-4aced7aa4316" />

<hr/>

<h2>3️⃣ Configure Coordinates in <code>variable.py</code></h2>

<p>
  You will see many variables, but only the following are important:
</p>

<ul>
  <li><code>TESSERACT_CMD</code> – Path to Tesseract OCR</li>
  <li><code>TOWER_ICON</code>, <code>MOD_ICON</code>, <code>MOD_TO_ROLL_ICON</code></li>
  <li><code>MOD_OPTIONS</code> & <code>MOD_OPTIONS_DEBUG</code> (same coordinates)</li>
  <li><code>REROLL_EFFECTS</code></li>
  <li><code>AUTO_REROLL_BUTTON</code></li>
  <li><code>EXIT_TOWER_BUTTON</code> (small X on LDPlayer)</li>
  <li><code>AUTO_REROLL_TEXT_REGION</code></li>
  <li><code>LOADING_SCREEN_CHECK_REGION</code></li>
</ul>

<p>
  <b>AFTER_ROLL_COORDS</b> contains:
</p>

<ul>
  <li><b>exit_icon</b> – X button</li>
  <li><b>check_icon</b> – New button</li>
  <li><b>Sublock</b> – OCR check for Ancestral substat</li>
  <li><b>Lockicon</b> – Lock button position</li>
  <li><b>LockIconImage</b> – Detect locked / unlocked state</li>
</ul>

<hr/>

<h2>4️⃣ Verify Coordinates with <code>calibration.py</code></h2>

<p>
  In <code>check_location()</code>, change:
</p>

<pre>
calibrate_pointer(cfg.MOD_OPTIONS)
</pre>

<p>
  to any button you want to verify (Tower icon, Mod icon, etc).
</p>

<p>
  The <b>for loop</b> checks all substat regions:
</p>

<ul>
  <li>If OCR prints <b>"Ancestrial"</b> (no strange characters like <code>|</code> or <code>)</code>)</li>
  <li>And unlocked sub color equals <code>#494675</code></li>
</ul>

<p>
  👉 Then everything is ready.  
  Otherwise, manually adjust values in <code>AFTER_ROLL_COORDS</code>.
</p>

<hr/>

<h2>5️⃣ Start Auto Rerolling</h2>

<ul>
  <li>
    Create a <code>.env</code> file in the same directory as <code>reroll.py</code>
  </li>
</ul>

<pre>
BARK_KEY=your_bark_key
TESSERACT_PATH=your_tesseract_path
</pre>

<ul>
  <li>
    In <code>reroll.py</code>, change:
    <pre>cfg = variable.Layout_241</pre>
    to your desired layout (<code>161</code>, <code>201</code>, or <code>241</code>)
  </li>

  <li>In LDPlayer, choose exactly all the number of sub you want to roll in that "Select sub" type (either core, gen, ...), cloud save, exit the Tower and return to the main screen</li>
  <li>Start the program, then quickly switch to LDPlayer</li>
</ul>

<p>
  🎉 Sit back, relax, and enjoy your fully rolled mod!  
  (It may take anywhere from <b>30 minutes to several hours</b>.)
</p>

<p>
  📱 Once completed, a notification will be sent to your iPhone via Bark.
</p>
