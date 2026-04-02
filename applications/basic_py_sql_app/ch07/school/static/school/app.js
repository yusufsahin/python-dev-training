(function () {
  "use strict";

  function showModal(id) {
    var el = document.getElementById(id);
    if (el && typeof bootstrap !== "undefined") {
      new bootstrap.Modal(el).show();
    }
  }

  function initDeptList() {
    var cfg = window.__DEPT_LIST__;
    if (!cfg) return;

    if (cfg.showCreate) showModal("modalDeptCreate");
    if (cfg.showEdit) showModal("modalDeptEdit");

    document.querySelectorAll("[data-action=\"dept-edit\"]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var idInput = document.getElementById("dept_edit_pk");
        var nameInput = document.getElementById("dept_edit-name");
        if (idInput) idInput.value = btn.getAttribute("data-id") || "";
        if (nameInput) nameInput.value = btn.getAttribute("data-name") || "";
        showModal("modalDeptEdit");
      });
    });

    document.querySelectorAll("[data-action=\"dept-delete\"]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var pk = document.getElementById("delete_dept_pk");
        var lbl = document.getElementById("delete_dept_label");
        if (pk) pk.value = btn.getAttribute("data-id") || "";
        if (lbl) lbl.textContent = btn.getAttribute("data-name") || "";
      });
    });
  }

  function initStudentList() {
    var cfg = window.__STU_LIST__;
    if (!cfg) return;

    if (cfg.showCreate) showModal("modalStuCreate");
    if (cfg.showEdit) showModal("modalStuEdit");

    document.querySelectorAll("[data-action=\"stu-edit\"]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var pk = document.getElementById("stu_edit_pk");
        if (pk) pk.value = btn.getAttribute("data-id") || "";
        var n = document.getElementById("stu_edit-student_number");
        if (n) n.value = btn.getAttribute("data-number") || "";
        var fn = document.getElementById("stu_edit-first_name");
        if (fn) fn.value = btn.getAttribute("data-first") || "";
        var ln = document.getElementById("stu_edit-last_name");
        if (ln) ln.value = btn.getAttribute("data-last") || "";
        var bd = document.getElementById("stu_edit-birth_date");
        if (bd) bd.value = btn.getAttribute("data-birth") || "";
        var dep = document.getElementById("stu_edit-department");
        if (dep) dep.value = btn.getAttribute("data-department") || "";
        showModal("modalStuEdit");
      });
    });

    document.querySelectorAll("[data-action=\"stu-delete\"]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var pk = document.getElementById("delete_stu_pk");
        var lbl = document.getElementById("delete_stu_label");
        if (pk) pk.value = btn.getAttribute("data-id") || "";
        if (lbl) lbl.textContent = btn.getAttribute("data-name") || "";
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initDeptList();
    initStudentList();
  });
})();
