<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Piping Support Span Calculator</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f7f6;
            color: #333;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: #fff;
            padding: 20px 30px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        h2 {
            text-align: center;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        .input-group {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 20px;
        }
        .input-box {
            flex: 1 1 45%;
            display: flex;
            flex-direction: column;
        }
        label {
            font-weight: bold;
            margin-bottom: 5px;
            color: #555;
        }
        input {
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: #3498db;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background-color: #2980b9;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #2c3e50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .validation-box {
            margin-top: 20px;
            padding: 15px;
            border-radius: 4px;
            font-weight: bold;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>

<div class="container">
    <h2>Piping Support Layout Generator</h2>
    
    <div class="input-group">
        <div class="input-box">
            <label>Total Pipe Length (m):</label>
            <input type="number" id="totalLength" value="50">
        </div>
        <div class="input-box">
            <label>Base Span [1.0 * L] (m):</label>
            <input type="number" id="baseSpan" value="7.8" step="0.1">
        </div>
        <div class="input-box">
            <label>Valve Location (m):</label>
            <input type="number" id="valveLoc" value="30">
        </div>
        <div class="input-box">
            <label>Elbow Location (m):</label>
            <input type="number" id="elbowLoc" value="40">
        </div>
    </div>

    <button onclick="calculateLayout()">Calculate Supports</button>

    <div id="outputArea" style="display: none;">
        <table>
            <thead>
                <tr>
                    <th>Support No.</th>
                    <th>Location (m)</th>
                    <th>Rule Applied</th>
                </tr>
            </thead>
            <tbody id="tableBody"></tbody>
        </table>

        <div id="validationResult" class="validation-box"></div>
    </div>
</div>

<script>
function calculateLayout() {
    const totalLength = parseFloat(document.getElementById('totalLength').value);
    const baseSpan = parseFloat(document.getElementById('baseSpan').value);
    const valveLoc = parseFloat(document.getElementById('valveLoc').value);
    const elbowLoc = parseFloat(document.getElementById('elbowLoc').value);

    let supports = [];
    
    // Rule 1: First Support (0.85 * Span)
    let firstSupport = 0.85 * baseSpan;
    supports.push({ name: "S1", pos: firstSupport, rule: "End Flange (0.85 * Span)" });

    let currentPos = firstSupport;
    let count = 2;

    // Rule 2: Normal Spans before Valve
    while (currentPos + baseSpan < valveLoc - 0.5) {
        currentPos += baseSpan;
        supports.push({ name: `S${count}`, pos: currentPos, rule: "Normal Span (1.0 * Span)" });
        count++;
    }

    // Rule 3: Valve Supports (0.5m before and after valve)
    let valveUp = valveLoc - 0.5;
    let valveDown = valveLoc + 0.5;
    supports.push({ name: `S${count}`, pos: valveUp, rule: "Valve Upstream Support" });
    count++;
    supports.push({ name: `S${count}`, pos: valveDown, rule: "Valve Downstream Support" });
    count++;

    // Rule 4: End Support position (Total Length - 0.85*Span)
    let endSupportPos = totalLength - (0.85 * baseSpan);

    // Rule 5: Normal Spans after Valve
    currentPos = valveDown;
    while (currentPos + baseSpan < endSupportPos) {
        currentPos += baseSpan;
        supports.push({ name: `S${count}`, pos: currentPos, rule: "Normal Span (1.0 * Span)" });
        count++;
    }

    // Add End Support
    supports.push({ name: `S${count}`, pos: endSupportPos, rule: "End Flange (0.85 * Span)" });

    // --- Render Table ---
    let tableBody = document.getElementById("tableBody");
    tableBody.innerHTML = "";
    supports.forEach(sup => {
        let row = `<tr>
            <td><strong>${sup.name}</strong></td>
            <td>${sup.pos.toFixed(2)}</td>
            <td>${sup.rule}</td>
        </tr>`;
        tableBody.innerHTML += row;
    });

    // --- Elbow Rule Validation (0.75 * Span) ---
    let elbowLimit = 0.75 * baseSpan;
    
    // Find supports right before and after the elbow
    let supBeforeElbow = supports.filter(s => s.pos < elbowLoc).pop();
    let supAfterElbow = supports.find(s => s.pos > elbowLoc);
    
    let validationBox = document.getElementById("validationResult");
    
    if (supBeforeElbow && supAfterElbow) {
        let actualDist = supAfterElbow.pos - supBeforeElbow.pos;
        
        let msg = `<strong>Elbow Validation (0.75 * Span Rule):</strong><br>
                   Elbow Location: ${elbowLoc} m<br>
                   Supports near Elbow: ${supBeforeElbow.name} (${supBeforeElbow.pos.toFixed(2)}m) and ${supAfterElbow.name} (${supAfterElbow.pos.toFixed(2)}m)<br>
                   Actual Distance: ${actualDist.toFixed(2)} m <br>
                   Maximum Allowed Distance (0.75 * ${baseSpan}): ${elbowLimit.toFixed(2)} m <br><br>`;
                   
        if (actualDist <= elbowLimit) {
            validationBox.className = "validation-box success";
            validationBox.innerHTML = msg + "✅ SUCCESS: The distance is within the standard limit.";
        } else {
            validationBox.className = "validation-box error";
            validationBox.innerHTML = msg + "❌ FAILED: The distance exceeds standard limit. Adjust spans!";
        }
    } else {
         validationBox.className = "validation-box error";
         validationBox.innerHTML = "Error: Please check Elbow location. It should be between supports.";
    }

    // Show output
    document.getElementById("outputArea").style.display = "block";
}
</script>

</body>
</html>
