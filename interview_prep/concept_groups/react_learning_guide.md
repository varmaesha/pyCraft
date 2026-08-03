# React Learning Guide For Interview Prep

This guide is designed for a full-stack developer who is not actively working on frontend every day but wants a practical React refresher for frontend interviews.

It starts from the basics and moves toward common interview topics such as JSX, state, hooks, reconciliation, and performance optimization with memoization.

---

## 1. What is React?

**Short answer:**
- React is a JavaScript library for building user interfaces.
- It helps you build UI as a composition of small reusable components.
- React updates the UI efficiently by using a virtual DOM and reconciliation.

**Interview-style explanation:**
> React is a component-based UI library. Instead of manually mutating the DOM for every change, React keeps a lightweight virtual representation of the UI and updates only what is necessary.

**Simple mental model:**
- Component = a reusable UI block
- Props = data passed into a component
- State = internal data that can change over time

---

## 2. JSX Basics and Fragments

### What is JSX?
JSX is a syntax extension that lets you write HTML-like code inside JavaScript.

```jsx
const Greeting = () => <h1>Hello, React!</h1>;
```

### Why use fragments?
Fragments let you return multiple elements without adding extra wrapper nodes.

```jsx
const Example = () => (
  <>
    <h2>Title</h2>
    <p>Paragraph</p>
  </>
);
```

### Interview follow-up
- Why use fragments instead of a `<div>`?
- Because fragments do not add extra DOM nodes, which can be useful for layout simplicity and avoiding unnecessary wrappers.

---

## 3. Mini React Exercise: Word Frequency Counter

### Problem
Given a constant string:

```jsx
const text = "apple banana apple grape";
```

Write a small React component that counts the frequency of each word and renders it in JSX using a fragment.

### Example solution

```jsx
import React from "react";

const WordFrequency = () => {
  const text = "apple banana apple grape";
  const words = text.split(" ");

  const freqMap = words.reduce((acc, word) => {
    acc[word] = (acc[word] || 0) + 1;
    return acc;
  }, {});

  return (
    <>
      <h3>Word Frequency</h3>
      <ul>
        {Object.entries(freqMap).map(([word, count]) => (
          <li key={word}>
            {word}: {count}
          </li>
        ))}
      </ul>
    </>
  );
};

export default WordFrequency;
```

### What this teaches
- JSX syntax
- Using `reduce` to build a frequency map
- Rendering lists with `map`
- Using `key` in React lists
- Using fragments to return multiple elements

---

## 4. Props vs State

### Props
- Props are read-only inputs passed from parent to child.
- They are used to configure a component.

```jsx
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}
```

### State
- State is internal data that can change inside a component.
- It is usually managed with `useState`.

```jsx
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </>
  );
}
```

### Interview follow-up
- What is the difference between props and state?
- Props come from the parent and are immutable from the child’s perspective.
- State is local and can be updated by the component itself.

---

## 5. Controlled Components and Forms

A controlled component keeps form input values in React state.

```jsx
import { useState } from "react";

function LoginForm() {
  const [email, setEmail] = useState("");

  return (
    <form>
      <input
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <p>You entered: {email}</p>
    </form>
  );
}
```

### Why this matters
- It gives React full control over the form input state.
- It is easy to validate and submit.

---

## 6. Conditional Rendering

```jsx
function Status({ isLoggedIn }) {
  return isLoggedIn ? <p>Welcome back!</p> : <p>Please log in.</p>;
}
```

### Common patterns
- ternary operator
- `&&` operator
- early return

---

## 7. Rendering Lists and Keys

```jsx
const fruits = ["apple", "banana", "grape"];

function FruitList() {
  return (
    <ul>
      {fruits.map((fruit) => (
        <li key={fruit}>{fruit}</li>
      ))}
    </ul>
  );
}
```

### Important interview point
- The `key` prop helps React identify which items changed, were added, or removed.
- Keys should be stable and unique.

---

## 8. useEffect and Side Effects

`useEffect` runs after render and is useful for tasks like fetching data or subscribing to events.

```jsx
import { useEffect, useState } from "react";

function UserData() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("https://jsonplaceholder.typicode.com/todos/1")
      .then((res) => res.json())
      .then((json) => setData(json));
  }, []);

  return <pre>{data ? JSON.stringify(data, null, 2) : "Loading..."}</pre>;
}
```

### Important interview point
- Empty dependency array means run once after initial render.
- If dependencies change, the effect reruns.

---

## 9. useMemo and useCallback

### useMemo
Use it to memoize expensive computed values.

```jsx
import { useMemo, useState } from "react";

function ExpensiveComponent({ items }) {
  const [count, setCount] = useState(0);

  const filteredItems = useMemo(() => {
    return items.filter((item) => item.active);
  }, [items]);

  return (
    <>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <p>Count: {count}</p>
      <pre>{JSON.stringify(filteredItems, null, 2)}</pre>
    </>
  );
}
```

### useCallback
Use it to memoize function references and prevent unnecessary re-creation.

```jsx
import { useCallback, useState } from "react";

function Child({ onClick }) {
  return <button onClick={onClick}>Click me</button>;
}
```

### Interview explanation
- `useMemo` optimizes computed values.
- `useCallback` optimizes function identity.
- Use them only when there is a real performance need.

---

## 10. React Reconciliation and the Virtual DOM

### What is reconciliation?
React compares the previous rendered tree with the new one and updates only the changed parts.

### Why does this matter?
It helps React keep UI updates efficient without redoing the entire DOM structure each time.

### Simple analogy
- The virtual DOM is like a lightweight draft.
- React compares the draft with the current UI and only applies the differences.

### Interview-style answer
> Reconciliation is the process React uses to detect minimal changes between renders and update the DOM efficiently.

---

## 11. React.memo and Avoiding Full Table Re-renders

A common interview scenario is a large table where changing one row should not cause the whole table to re-render.

### Example

```jsx
import React, { memo } from "react";

const Row = memo(function Row({ row, onSelect }) {
  return (
    <tr>
      <td>{row.id}</td>
      <td>{row.name}</td>
      <td>{row.status}</td>
      <td>
        <button onClick={() => onSelect(row.id)}>Select</button>
      </td>
    </tr>
  );
});

function Table({ rows, selectedId, onSelect }) {
  return (
    <table>
      <tbody>
        {rows.map((row) => (
          <Row
            key={row.id}
            row={row}
            onSelect={onSelect}
            selectedId={selectedId}
          />
        ))}
      </tbody>
    </table>
  );
}
```

### Why `memo` helps
- `React.memo` prevents a component from re-rendering if its props have not changed.
- This can reduce unnecessary work when a large table contains many rows.

### Important note
- `memo` only helps if props are stable or shallow-equal.
- If a parent passes a new inline function or new object every render, memo may not help as much.

### Interview follow-up
- When would you use `memo`?
- When a child component is expensive to render and receives mostly unchanged props.
- What is the difference between `memo` and `useMemo`?
- `memo` avoids re-rendering components.
- `useMemo` avoids recomputing values.

---

## 12. Common React Interview Questions

### Q1. What is the difference between state and props?
- Props are passed from parent to child.
- State belongs to the component and can change.

### Q2. What is JSX?
- JSX is JavaScript syntax that looks like HTML and is compiled to React elements.

### Q3. Why is `key` important in lists?
- It helps React track items efficiently during updates.

### Q4. What is the difference between `useEffect` and `useLayoutEffect`?
- `useEffect` runs after paint.
- `useLayoutEffect` runs before the browser paints.

### Q5. What is reconciliation?
- It is the process React uses to compare renders and apply the minimum necessary DOM updates.

### Q6. What is the purpose of `React.memo`?
- It prevents unnecessary re-renders for components with unchanged props.

---

## 13. Quick Revision Checklist

Before an interview, make sure you can explain these confidently:
- What React is and why it is used
- JSX and fragments
- Props vs state
- Controlled forms
- Conditional rendering
- Lists and keys
- `useEffect`
- `useMemo` and `useCallback`
- Reconciliation
- `React.memo` and row-level optimization in large tables

---

## 14. Practical Interview Tip

When you answer React questions, try to connect the concept to a real-world example:
- A table with many rows
- A form with validation
- A dashboard with live updates
- A component that fetches data on mount

That makes your answer sound practical and not just theoretical.

---

## 15. Functional Components vs Class Components

### Functional components
Functional components are written as plain functions and are the modern React style.

```jsx
function Welcome({ name }) {
  return <h1>Hello, {name}</h1>;
}
```

They are simpler, easier to read, and work very well with hooks.

### Class components
Class components use `class extends React.Component` and lifecycle methods.

```jsx
class Welcome extends React.Component {
  render() {
    return <h1>Hello, {this.props.name}</h1>;
  }
}
```

### Why class components matter in interviews
Even though modern React mostly uses functional components, interviewers may still ask about:
- `componentDidMount`
- `componentDidUpdate`
- `componentWillUnmount`
- `this.setState`

### Use cases
- Functional components are preferred for new code.
- Class components are still relevant when reading older codebases or maintaining legacy systems.

### Memory trick
- Functional component = modern, simple, hook-friendly
- Class component = older, lifecycle-based, more verbose

---

## 16. Hooks in More Depth

### useState
Use it for simple local state.

```jsx
const [count, setCount] = useState(0);
```

### useEffect
Use it for side effects such as API calls, subscriptions, timers, or DOM updates.

```jsx
useEffect(() => {
  const timer = setTimeout(() => console.log("done"), 1000);
  return () => clearTimeout(timer);
}, []);
```

### useRef
Use it to keep mutable values without causing a re-render.

```jsx
const inputRef = useRef(null);
```

### useReducer
Use it when state logic becomes more complex.

```jsx
const [state, dispatch] = useReducer(reducer, initialState);
```

### useContext
Use it to consume values from context without prop drilling.

### useMemo and useCallback
These help optimize expensive calculations and callback identity.

### Rules of hooks
- Call hooks at the top level of a function.
- Do not call hooks inside loops, conditions, or nested functions.
- Hooks should be used only in React function components or custom hooks.

### Common interview follow-up
- What is a stale closure?
- A stale closure happens when a function captures an old value from a previous render.
- This often appears when a effect or callback depends on outdated state.

### Custom hooks
Custom hooks make logic reusable across components.

```jsx
function useCounter() {
  const [count, setCount] = useState(0);

  const increment = () => setCount((c) => c + 1);

  return { count, increment };
}
```

### Use case
A custom hook is great for reusable logic like fetching data, handling form state, or managing browser storage.

---

## 17. Modern React Concepts You Should Know

### Debouncing and throttling
Debouncing delays an action until a pause in events, which is useful for search boxes, autocomplete, and resize handlers.

```jsx
import { useEffect, useState } from "react";

function SearchBox() {
  const [query, setQuery] = useState("");

  useEffect(() => {
    const timer = setTimeout(() => {
      console.log("Search API called for:", query);
    }, 400);

    return () => clearTimeout(timer);
  }, [query]);

  return <input value={query} onChange={(e) => setQuery(e.target.value)} />;
}
```

### Why this matters in interviews
- Prevents too many API calls while the user is typing
- Improves performance and reduces unnecessary backend traffic
- Commonly asked in frontend interviews for real-world UX scenarios

### Suspense and lazy loading
Use `React.lazy` and `Suspense` to load components only when needed.

```jsx
const Dashboard = React.lazy(() => import("./Dashboard"));

<Suspense fallback={<div>Loading...</div>}>
  <Dashboard />
</Suspense>
```

### Error boundaries
Error boundaries catch rendering errors in a subtree and show fallback UI.

### Portals
Portals let you render children into a DOM node outside the parent component tree.

### Strict Mode
Strict Mode highlights potential problems by intentionally double-invoking mount effects in development.

### Why these matter in interviews
They show that you understand not just basic rendering, but also modern production-ready React patterns.

---

## 18. State Management: Local State, Context, Redux, and Beyond

### Local state
Best for simple components or UI state that does not need to be shared widely.

### Context API
Use it when many components need the same data without passing props everywhere.

```jsx
const ThemeContext = React.createContext();
```

### When Context is useful
- theme
- authentication state
- locale/language
- user preferences

### Redux
Redux is useful for larger applications with predictable state transitions.

Typical pieces:
- store
- actions
- reducers
- dispatch

### Why Redux is still asked in interviews
Even if a team uses modern alternatives, interviewers want to know whether you understand the core concepts of centralized state management.

### Zustand / Recoil / React Query
These are often used as lighter alternatives or complementary tools.
- Zustand: simple global state
- Recoil: atom-based state management
- React Query: server state caching and synchronization

### Server state vs client state
- Client state: UI state like modal open/closed
- Server state: data fetched from APIs, often cached and updated

This distinction is important because React Query or similar libraries are often used for server state.

---

## 19. Middleware and Side Effects: Redux Thunk vs Redux Saga

### What is middleware?
Middleware sits between dispatching an action and the reducer handling it. It is used for logging, async logic, and side effects.

### Redux Thunk
Thunk lets you write action creators that return functions instead of plain objects.

```js
const fetchUser = () => (dispatch) => {
  dispatch({ type: "FETCH_START" });
  fetch("/api/user")
    .then((res) => res.json())
    .then((data) => dispatch({ type: "FETCH_SUCCESS", payload: data }));
};
```

### Why people use thunk
- simple async logic
- easy to understand for small apps

### Redux Saga
Saga uses generator functions to manage complex side effects in a more declarative way.

```js
function* watchFetchUser() {
  yield takeEvery("FETCH_USER_REQUEST", fetchUser);
}

function* fetchUser() {
  try {
    const user = yield call(api.getUser);
    yield put({ type: "FETCH_USER_SUCCESS", payload: user });
  } catch (error) {
    yield put({ type: "FETCH_USER_FAILURE", error });
  }
}
```

### Why saga is useful
- handles complex async flows
- easier to test
- good for retry, cancellation, multiple dependent API requests, or long-running workflows

### Interview-style explanation
> Redux Saga is a middleware library for managing side effects in a predictable and testable way, especially when your app has complex workflows such as authentication, checkout, or multi-step forms.

### Memory trick
- Thunk = simpler, function-based async logic
- Saga = more structured, generator-based workflow control

---

## 20. High-Value Interview Questions and Model Answers

### Q1. What is the difference between props and state?
Answer:
- Props are passed from parent to child and are read-only from the child’s point of view.
- State is local and can change over time.

### Q2. Why do we need keys in lists?
Answer:
- Keys help React identify which items changed, were added, or removed.
- Without stable keys, React can perform inefficient updates and produce unexpected UI behavior.

### Q3. What is reconciliation?
Answer:
- Reconciliation is the process React uses to compare the previous and new virtual trees and apply the minimal DOM updates.

### Q4. What is the difference between `useEffect` and event handlers?
Answer:
- Event handlers respond to user actions like clicks.
- `useEffect` is used for side effects that happen after render, such as data fetching or subscriptions.

### Q5. Why would you use `React.memo`?
Answer:
- To prevent unnecessary re-renders of components when props are unchanged.
- This is useful for large lists, tables, and expensive child components.

### Q6. What is the difference between `useMemo` and `useCallback`?
Answer:
- `useMemo` memoizes values.
- `useCallback` memoizes functions.

### Q7. What is prop drilling?
Answer:
- Prop drilling is when data is passed through many levels of components even though only a deeply nested child needs it.
- Context API or state libraries can reduce this problem.

### Q8. What is a custom hook?
Answer:
- A custom hook is a reusable function that groups reusable logic and uses React hooks internally.

### Q9. What is the difference between local state, Context, and Redux?
Answer:
- Local state is best for simple component-level state.
- Context is good for shared data across a subtree.
- Redux is useful for large, predictable, and centralized state management.

### Q10. Why is Redux Saga still relevant?
Answer:
- It helps manage complex asynchronous workflows in a testable way.
- It is especially useful for multi-step flows such as checkout, login, or approval systems.

---

## 21. Quick Study Memory Map

If you are preparing for interviews, remember these categories:
- Basics: JSX, components, props, state
- Rendering: lists, keys, conditional rendering
- Hooks: `useState`, `useEffect`, `useRef`, `useReducer`
- Performance: `memo`, `useMemo`, `useCallback`
- Architecture: Context, Redux, saga, React Query
- Modern React: Suspense, lazy loading, Error Boundaries, Portals

### One-line memory anchors
- Components build UI
- Props flow down, state changes up or within
- Hooks make function components powerful
- Reconciliation makes updates efficient
- Memoization avoids unnecessary work
- Middleware helps handle side effects cleanly

---

## 22. Final Interview Tip

When you answer React questions, speak in terms of trade-offs:
- Why choose local state vs Context vs Redux
- Why use hooks instead of class components in new code
- When memoization is worth it and when it is overkill
- How to handle side effects safely and predictably

Interviewers usually value clarity, practical examples, and good reasoning more than memorizing syntax alone.
