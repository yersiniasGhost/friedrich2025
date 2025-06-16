// Add to static/js/photos.js

document.addEventListener('DOMContentLoaded', function() {
  initPhotoUpload();
  initPhotoGallery();
  initLightbox();
});

// Photo Upload Functionality
function initPhotoUpload() {
  const fileInput = document.getElementById('photo');
  const dropZone = document.querySelector('.upload-dropzone');
  const previewElement = document.getElementById('preview-image');
  const previewPlaceholder = document.getElementById('preview-placeholder');

  if (!fileInput || !dropZone) return;

  // Handle file input change
  fileInput.addEventListener('change', function(e) {
    handleFileSelect(e);
  });

  // Drag and drop functionality
  dropZone.addEventListener('dragover', function(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.add('drag-active');
  });

  dropZone.addEventListener('dragleave', function(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('drag-active');
  });

  dropZone.addEventListener('drop', function(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('drag-active');

    if (e.dataTransfer.files.length) {
      fileInput.files = e.dataTransfer.files;
      handleFileSelect({ target: fileInput });
    }
  });

  // Handle file selection
  function handleFileSelect(e) {
    const file = e.target.files[0];

    if (!file) return;

    // Check file type
    const fileType = file.type;
    if (!['image/jpeg', 'image/jpg', 'image/png', 'image/gif'].includes(fileType)) {
      alert('Please select a valid image file (JPEG, PNG, or GIF)');
      return;
    }

    // Check file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      alert('File size should not exceed 10MB');
      return;
    }

    // Create preview
    const reader = new FileReader();
    reader.onload = function(e) {
      if (previewElement && previewPlaceholder) {
        previewElement.src = e.target.result;
        previewElement.classList.remove('hidden');
        previewPlaceholder.classList.add('hidden');
      }
    };
    reader.readAsDataURL(file);
  }
}

// Photo Gallery Functionality
function initPhotoGallery() {
  const gallery = document.querySelector('.photo-grid');
  const voteButtons = document.querySelectorAll('.vote-button');

  if (!gallery) return;

  // Handle vote button clicks
  voteButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      if (button.disabled) {
        e.preventDefault();
        alert('You have no votes remaining for this week');
      }
    });
  });

  // Handle lazy loading of images
  if ('IntersectionObserver' in window) {
    const lazyImages = document.querySelectorAll('.lazy-image');

    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const image = entry.target;
          image.src = image.dataset.src;
          image.classList.remove('lazy-image');
          imageObserver.unobserve(image);
        }
      });
    });

    lazyImages.forEach(image => {
      imageObserver.observe(image);
    });
  }
}

// Lightbox Functionality
function initLightbox() {
  const galleryImages = document.querySelectorAll('.gallery-image');
  const lightbox = document.querySelector('.photo-lightbox');
  const lightboxImage = document.querySelector('.lightbox-image');
  const lightboxCaption = document.querySelector('.lightbox-caption');
  const lightboxClose = document.querySelector('.lightbox-close');

  if (!galleryImages.length || !lightbox) return;

  // Create lightbox if it doesn't exist
  if (!lightbox) {
    const lightboxHTML = `
      <div class="photo-lightbox">
        <div class="lightbox-content">
          <img class="lightbox-image" src="" alt="Full size image">
          <div class="lightbox-caption"></div>
          <div class="lightbox-close">×</div>
        </div>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', lightboxHTML);

    // Now select the newly created elements
    lightbox = document.querySelector('.photo-lightbox');
    lightboxImage = document.querySelector('.lightbox-image');
    lightboxCaption = document.querySelector('.lightbox-caption');
    lightboxClose = document.querySelector('.lightbox-close');
  }

  // Open lightbox when clicking on gallery images
  galleryImages.forEach(image => {
    image.addEventListener('click', function() {
      const fullSrc = this.dataset.fullSrc || this.src;
      const caption = this.alt || this.dataset.caption || '';

      lightboxImage.src = fullSrc;
      lightboxCaption.textContent = caption;
      lightbox.classList.add('active');
      document.body.style.overflow = 'hidden'; // Prevent scrolling while lightbox is open
    });
  });

  // Close lightbox
  if (lightboxClose) {
    lightboxClose.addEventListener('click', closeLightbox);
  }

  if (lightbox) {
    lightbox.addEventListener('click', function(e) {
      if (e.target === lightbox) {
        closeLightbox();
      }
    });
  }

  // Close lightbox with escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && lightbox.classList.contains('active')) {
      closeLightbox();
    }
  });

  function closeLightbox() {
    lightbox.classList.remove('active');
    document.body.style.overflow = ''; // Restore scrolling

    // Clear src after animation completes to prevent unnecessary bandwidth usage
    setTimeout(() => {
      lightboxImage.src = '';
    }, 300);
  }
}

// Countdown timer for contest deadline
function initContestCountdown() {
  const countdownElement = document.getElementById('contest-countdown');
  if (!countdownElement) return;

  const deadlineDate = countdownElement.dataset.deadline;
  if (!deadlineDate) return;

  const deadline = new Date(deadlineDate).getTime();

  const countdownTimer = setInterval(function() {
    const now = new Date().getTime();
    const distance = deadline - now;

    // Time calculations
    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Display the result
    countdownElement.innerHTML = `
      <span class="countdown-unit">${days}d</span>
      <span class="countdown-unit">${hours}h</span>
      <span class="countdown-unit">${minutes}m</span>
      <span class="countdown-unit">${seconds}s</span>
    `;

    // If the countdown is finished
    if (distance < 0) {
      clearInterval(countdownTimer);
      countdownElement.innerHTML = '<span class="text-red-500">Contest has ended</span>';
    }
  }, 1000);
}

// Animated vote confirmation
function animateVote(buttonElement) {
  if (!buttonElement) return;

  // Add temporary disabled state
  buttonElement.disabled = true;

  // Store original text
  const originalText = buttonElement.textContent;

  // Change text and style
  buttonElement.innerHTML = '<span class="vote-animation">Voted ✓</span>';
  buttonElement.classList.add('voted');

  // Animate counter increment if applicable
  const counterElement = document.querySelector('.vote-count');
  if (counterElement) {
    const currentCount = parseInt(counterElement.textContent || '0');
    counterElement.textContent = currentCount + 1;

    // Add animation class
    counterElement.classList.add('vote-increment');
    setTimeout(() => {
      counterElement.classList.remove('vote-increment');
    }, 1000);
  }

  // Update votes remaining indicator
  const votesRemainingElement = document.getElementById('votes-remaining');
  if (votesRemainingElement) {
    const remainingVotes = parseInt(votesRemainingElement.textContent || '0');
    if (remainingVotes > 0) {
      votesRemainingElement.textContent = remainingVotes - 1;
    }
  }
}