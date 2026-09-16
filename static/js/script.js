document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById("sidebarToggle");
  const sidebar = document.getElementById("appSidebar");
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener("click", function () {
      sidebar.classList.toggle("open");
    });
    document.querySelectorAll(".sidebar-link").forEach(function (link) {
      link.addEventListener("click", function () {
        if (window.innerWidth <= 900) sidebar.classList.remove("open");
      });
    });
  }

  document.querySelectorAll(".alert-auto-dismiss").forEach(function (alertEl) {
    setTimeout(function () {
      const instance = bootstrap.Alert.getOrCreateInstance(alertEl);
      instance.close();
    }, 4500);
  });
});

function confirmDelete(message) {
  return confirm(message || "Are you sure you want to delete this item?");
}
