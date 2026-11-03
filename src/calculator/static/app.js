document.addEventListener("DOMContentLoaded", () => {
  const mainDisplay = document.getElementById("main-display");
  const exprDisplay = document.getElementById("expr-display");
  const memIndicator = document.getElementById("mem-indicator");
  const historyList = document.getElementById("history-list");
  const clearHistoryBtn = document.getElementById("clear-history-btn");

  let currentInput = "0";
  let hasEvaluated = false;

  function updateDisplay() {
    mainDisplay.textContent = currentInput;
  }

  function appendChar(ch) {
    if (hasEvaluated && !"+-*/%^".includes(ch)) {
      currentInput = ch;
    } else {
      if (currentInput === "0" && ch !== ".") {
        currentInput = ch;
      } else {
        currentInput += ch;
      }
    }
    hasEvaluated = false;
    updateDisplay();
  }

  function backspace() {
    if (hasEvaluated) {
      clearAll();
      return;
    }
    if (currentInput.length > 1) {
      currentInput = currentInput.slice(0, -1);
    } else {
      currentInput = "0";
    }
    updateDisplay();
  }

  function clearAll() {
    currentInput = "0";
    exprDisplay.textContent = "";
    hasEvaluated = false;
    updateDisplay();
  }

  async function evaluateExpression() {
    const expr = currentInput;
    exprDisplay.textContent = `${expr} =`;
    try {
      const res = await fetch("/api/evaluate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ expression: expr })
      });
      const data = await res.json();
      if (!res.ok) {
        mainDisplay.textContent = data.error || "Error";
        hasEvaluated = true;
      } else {
        currentInput = String(data.result);
        hasEvaluated = true;
        updateDisplay();
        loadHistory();
      }
    } catch (err) {
      mainDisplay.textContent = "Network Error";
      hasEvaluated = true;
    }
  }

  async function handleMemory(action) {
    try {
      const res = await fetch("/api/memory", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: action })
      });
      const data = await res.json();
      if (res.ok) {
        if (data.memory !== 0) {
          memIndicator.style.display = "inline-block";
        } else {
          memIndicator.style.display = "none";
        }
        if (action === "recall") {
          currentInput = String(data.current_value);
          hasEvaluated = true;
          updateDisplay();
        }
      }
    } catch (err) {
      console.error("Memory error:", err);
    }
  }

  async function loadHistory() {
    try {
      const res = await fetch("/api/history");
      const data = await res.json();
      if (res.ok && data.history) {
        renderHistory(data.history);
      }
    } catch (err) {
      console.error("Failed to load history", err);
    }
  }

  function renderHistory(items) {
    historyList.innerHTML = "";
    if (!items || items.length === 0) {
      historyList.innerHTML = '<li class="empty-state">No calculations yet.</li>';
      return;
    }

    [...items].reverse().forEach(item => {
      const li = document.createElement("li");
      li.className = "history-item";
      li.innerHTML = `
        <span class="hist-expr">${item.expression}</span>
        <span class="hist-res">${item.result}</span>
      `;
      li.addEventListener("click", () => {
        currentInput = String(item.result);
        hasEvaluated = true;
        updateDisplay();
      });
      historyList.appendChild(li);
    });
  }

  async function clearHistory() {
    try {
      await fetch("/api/clear_history", { method: "POST" });
      loadHistory();
    } catch (err) {
      console.error("Failed to clear history", err);
    }
  }

  // Event Delegation for buttons
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn) return;

    const val = btn.dataset.val;
    const action = btn.dataset.action;

    if (val) {
      appendChar(val);
    } else if (action === "clear") {
      clearAll();
    } else if (action === "backspace") {
      backspace();
    } else if (action === "equals") {
      evaluateExpression();
    } else if (action === "sqrt") {
      currentInput = `sqrt(${currentInput})`;
      evaluateExpression();
    } else if (action === "mc") {
      handleMemory("clear");
    } else if (action === "mr") {
      handleMemory("recall");
    } else if (action === "ms") {
      handleMemory("store");
    } else if (action === "m-plus") {
      handleMemory("add");
    } else if (action === "m-minus") {
      handleMemory("subtract");
    }
  });

  clearHistoryBtn.addEventListener("click", clearHistory);

  // Keyboard navigation
  document.addEventListener("keydown", (e) => {
    if (e.key >= "0" && e.key <= "9") {
      appendChar(e.key);
    } else if ("+-*/().^%".includes(e.key)) {
      appendChar(e.key);
    } else if (e.key === "Enter" || e.key === "=") {
      e.preventDefault();
      evaluateExpression();
    } else if (e.key === "Backspace") {
      backspace();
    } else if (e.key === "Escape") {
      clearAll();
    }
  });

  // Initial loads
  loadHistory();
});
