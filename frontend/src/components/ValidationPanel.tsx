import { useState } from 'react';

import { validateIdea } from '../services/api';

export function ValidationPanel() {
  const [form, setForm] = useState({ idea_title: '', idea_description: '', lob: '' });
  const [result, setResult] = useState<any>(null);

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    const response = await validateIdea(form);
    setResult(response);
  };

  return (
    <section>
      <h2>Validation Agent</h2>
      <form onSubmit={submit}>
        <input placeholder="Idea title" value={form.idea_title} onChange={(event) => setForm({ ...form, idea_title: event.target.value })} required />
        <input placeholder="LOB" value={form.lob} onChange={(event) => setForm({ ...form, lob: event.target.value })} required />
        <textarea placeholder="Idea description" value={form.idea_description} onChange={(event) => setForm({ ...form, idea_description: event.target.value })} required />
        <button type="submit">Validate</button>
      </form>

      {result && (
        <div>
          <p>Semantic Group: {result.semantic_group}</p>
          <p>LOB Match: {result.in_lob_match ? 'Yes' : 'No'}</p>
          <p>Suggested Contact: {result.recommended_partner_contact ?? 'N/A'}</p>
        </div>
      )}
    </section>
  );
}
