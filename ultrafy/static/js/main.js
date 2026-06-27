/* Ultrafy Fiber Network — Main JS */

document.addEventListener('DOMContentLoaded', function () {

  // ── Mobile Nav Toggle ──────────────────────────────────────
  const hamburger = document.querySelector('.uf-nav-hamburger');
  const navLinks  = document.querySelector('.uf-nav-links');

  if (hamburger && navLinks) {
    hamburger.addEventListener('click', function () {
      navLinks.classList.toggle('open');
      const spans = hamburger.querySelectorAll('span');
      hamburger.classList.toggle('active');
    });

    // Close on outside click
    document.addEventListener('click', function (e) {
      if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
        navLinks.classList.remove('open');
        hamburger.classList.remove('active');
      }
    });
  }

  // ── Active nav link ────────────────────────────────────────
  const path = window.location.pathname;
  document.querySelectorAll('.uf-nav-links a').forEach(function (link) {
    if (link.getAttribute('href') === path) {
      link.classList.add('active');
    }
  });

  // ── Auto-dismiss alerts ────────────────────────────────────
  setTimeout(function () {
    document.querySelectorAll('.uf-alert').forEach(function (el) {
      el.style.transition = 'opacity 0.4s ease, max-height 0.4s ease';
      el.style.opacity = '0';
      setTimeout(function () { el.remove(); }, 400);
    });
  }, 5000);

  // ── Amenities tag input ────────────────────────────────────
  const amenitiesInput = document.getElementById('amenities-input');
  const amenitiesHidden = document.getElementById('id_amenities_hidden');
  const amenitiesDisplay = document.getElementById('amenities-display');

  if (amenitiesInput && amenitiesHidden && amenitiesDisplay) {
    let amenities = [];

    function renderAmenities() {
      amenitiesDisplay.innerHTML = '';
      amenities.forEach(function (a, i) {
        const tag = document.createElement('span');
        tag.className = 'tag';
        tag.style.cursor = 'pointer';
        tag.textContent = a + ' ×';
        tag.addEventListener('click', function () {
          amenities.splice(i, 1);
          renderAmenities();
        });
        amenitiesDisplay.appendChild(tag);
      });
      amenitiesHidden.value = amenities.join(',');
    }

    amenitiesInput.addEventListener('keydown', function (e) {
      if ((e.key === 'Enter' || e.key === ',') && amenitiesInput.value.trim()) {
        e.preventDefault();
        const val = amenitiesInput.value.trim().replace(/,/g, '');
        if (val && !amenities.includes(val)) {
          amenities.push(val);
          renderAmenities();
        }
        amenitiesInput.value = '';
      }
    });
  }

  // ── Image preview on upload ────────────────────────────────
  const imageUpload = document.getElementById('id_images');
  const previewGrid = document.getElementById('image-preview-grid');

  if (imageUpload && previewGrid) {
    imageUpload.addEventListener('change', function () {
      previewGrid.innerHTML = '';
      Array.from(this.files).forEach(function (file) {
        if (!file.type.startsWith('image/')) return;
        const reader = new FileReader();
        reader.onload = function (e) {
          const div = document.createElement('div');
          div.style.cssText = 'border-radius:8px;overflow:hidden;aspect-ratio:4/3;background:#f0faf5;';
          const img = document.createElement('img');
          img.src = e.target.result;
          img.style.cssText = 'width:100%;height:100%;object-fit:cover;';
          div.appendChild(img);
          previewGrid.appendChild(div);
        };
        reader.readAsDataURL(file);
      });
    });
  }

  // ── Gallery lightbox (simple) ──────────────────────────────
  const galleryImgs = document.querySelectorAll('.gallery-thumb');
  const mainImg     = document.querySelector('.gallery-main-img');

  if (galleryImgs.length && mainImg) {
    galleryImgs.forEach(function (thumb) {
      thumb.addEventListener('click', function () {
        mainImg.src = this.src;
        galleryImgs.forEach(function (t) { t.classList.remove('active-thumb'); });
        this.classList.add('active-thumb');
      });
    });
  }

  // ── Scroll animations ──────────────────────────────────────
  if ('IntersectionObserver' in window) {
    const fadeEls = document.querySelectorAll('[data-fade]');
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });

    fadeEls.forEach(function (el) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(24px)';
      el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      observer.observe(el);
    });
  }

  // ── Confirm delete ─────────────────────────────────────────
  document.querySelectorAll('[data-confirm]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (!confirm(this.getAttribute('data-confirm'))) {
        e.preventDefault();
      }
    });
  });

});
