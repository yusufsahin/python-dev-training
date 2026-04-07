(function () {
  "use strict";

  function showModal(id) {
    var el = document.getElementById(id);
    if (el && typeof bootstrap !== "undefined") {
      new bootstrap.Modal(el).show();
    }
  }

  function initTaskList() {
    var cfg = window.__TASK_LIST__;
    if (!cfg) return;

    if (cfg.showCreate) showModal("modalTaskCreate");
    if (cfg.showEdit) showModal("modalTaskEdit");

    document.querySelectorAll("[data-action=\"task-edit\"]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var pk = document.getElementById("task_edit_pk");
        if (pk) pk.value = btn.getAttribute("data-id") || "";
        var title = document.getElementById("task_edit-title");
        if (title) title.value = btn.getAttribute("data-title") || "";
        var st = document.getElementById("task_edit-status");
        if (st) st.value = btn.getAttribute("data-status") || "todo";
        var sd = document.getElementById("task_edit-start_date");
        if (sd) sd.value = btn.getAttribute("data-start") || "";
        var ed = document.getElementById("task_edit-end_date");
        if (ed) ed.value = btn.getAttribute("data-end") || "";
        showModal("modalTaskEdit");
      });
    });

    document.querySelectorAll("[data-action=\"task-delete\"]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var pk = document.getElementById("delete_task_pk");
        var lbl = document.getElementById("delete_task_label");
        if (pk) pk.value = btn.getAttribute("data-id") || "";
        if (lbl) lbl.textContent = btn.getAttribute("data-title") || "";
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initTaskList();
  });
})();
