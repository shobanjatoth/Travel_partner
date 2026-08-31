/**
 * Travel Planning Dashboard Module
 */
let currentThreadId = null;

async function generatePlan() {
  const inputEl = document.getElementById('userQuery');
  const query = inputEl.value.trim();

  if (!query) return alert('Please enter a destination or travel details!');

  toggleLoading(true);
  hideResponseCard();

  const payload = { message: query };
  if (currentThreadId) {
    payload.thread_id = currentThreadId;
  }

  const res = await apiRequest('/travel', 'POST', payload);
  toggleLoading(false);

  if (res && res.ok) {
    currentThreadId = res.data.thread_id;
    renderItinerary(res.data);
  } else {
    alert('Failed to generate plan: ' + (res?.data?.detail || 'Server error'));
  }
}

async function sendApproval(approved) {
  if (!currentThreadId) return alert('No active session thread found.');

  const feedback = document.getElementById('humanFeedback').value.trim();
  if (!approved && !feedback) {
    return alert('Please enter feedback when requesting revisions.');
  }

  toggleLoading(true);

  const payload = {
    thread_id: currentThreadId,
    approved: approved,
    feedback: feedback
  };

  const res = await apiRequest('/travel/approve', 'POST', payload);
  toggleLoading(false);

  if (res && res.ok) {
    renderItinerary(res.data);
  } else {
    alert('Approval processing failed: ' + (res?.data?.detail || 'Error'));
  }
}

function renderItinerary(data) {
  const container = document.getElementById('responseContainer');
  const outputDiv = document.getElementById('formattedOutput');
  const banner = document.getElementById('approvalBanner');

  outputDiv.innerHTML = marked.parse(data.answer || 'No details generated.');
  container.classList.remove('hidden');

  if (data.requires_approval) {
    banner.classList.remove('hidden');
  } else {
    banner.classList.add('hidden');
    document.getElementById('humanFeedback').value = '';
  }
}

function toggleLoading(isLoading) {
  const loader = document.getElementById('loadingState');
  const btn = document.getElementById('submitBtn');
  if (isLoading) {
    loader.classList.remove('hidden');
    btn.disabled = true;
    btn.classList.add('opacity-50');
  } else {
    loader.classList.add('hidden');
    btn.disabled = false;
    btn.classList.remove('opacity-50');
  }
}

function hideResponseCard() {
  document.getElementById('responseContainer').classList.add('hidden');
  document.getElementById('approvalBanner').classList.add('hidden');
}