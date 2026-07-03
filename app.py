from flask import Flask, render_template, request, redirect, jsonify, send_file

from services.abuseipdb import check_ip
from services.geoip import get_location
from services.virustotal import check_ip as vt_check_ip

from database import (
    init_db,
    save_search,
    get_history,
    clear_history,
    delete_history_item,
    get_statistics
)

from report import generate_pdf

app = Flask(__name__)

init_db()


# ==========================
# Home Page
# ==========================
@app.route("/", methods=["GET"])
def home():

    history = get_history()
    stats = get_statistics()

    return render_template(
        "index.html",
        history=history,
        stats=stats
    )


# ==========================
# Search IP
# ==========================
@app.route("/search", methods=["POST"])
def search_ip():

    ip = request.form.get("ip", "").strip()

    if not ip:
        return jsonify({
            "success": False,
            "error": "IP Address is required."
        })

    result = check_ip(ip)

    if not result or result.get("error") or "data" not in result:
        return jsonify({
            "success": False,
            "error": "Invalid IP Address or AbuseIPDB API Error."
        })

    geo = get_location(ip)
    vt = vt_check_ip(ip)

    score = result["data"]["abuseConfidenceScore"]

    if score == 0:
        threat = "Safe"
        color = "success"

    elif score < 50:
        threat = "Suspicious"
        color = "warning"

    else:
        threat = "Malicious"
        color = "danger"

    # Save Search
    save_search(ip, threat, score)

    history = get_history()
    stats = get_statistics()

    return jsonify({

        "success": True,

        "result": result,

        "geo": geo,

        "vt": vt,

        "threat": threat,

        "color": color,

        "history": history,

        "stats": stats

    })


# ==========================
# Clear History
# ==========================
@app.route("/clear", methods=["POST"])
def clear():

    clear_history()

    return redirect("/")


# ==========================
# Delete One Record
# ==========================
@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):

    delete_history_item(item_id)

    return jsonify({
        "success": True
    })


# ==========================
# Download PDF
# ==========================
@app.route("/download-pdf")
def download_pdf():

    ip = request.args.get("ip")

    threat = request.args.get("threat")

    try:
        score = int(request.args.get("score", 0))
    except:
        score = 0

    geo = get_location(ip) or {}

    vt = vt_check_ip(ip)

    file_path = generate_pdf(
        ip,
        threat,
        score,
        geo,
        vt
    )

    return send_file(
        file_path,
        as_attachment=True
    )


# ==========================
# Run
# ==========================
if __name__ == "__main__":

    app.run(debug=True)