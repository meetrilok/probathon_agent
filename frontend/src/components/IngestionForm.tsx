import { useState } from 'react';

import { ingestUseCase } from '../services/api';

interface Props {
  onSuccess: () => void;
}

export function IngestionForm({ onSuccess }: Props) {
  const [form, setForm] = useState({
    title: '',
    description: '',
    lob: '',
    source_type: 'manual',
    contact_email: '',
    source_uri: '',
  });

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    await ingestUseCase(form);
    onSuccess();
    setForm({ ...form, title: '', description: '', lob: '' });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Ingest Use Case</h2>
      <input placeholder="Title" value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} required />
      <input placeholder="LOB" value={form.lob} onChange={(event) => setForm({ ...form, lob: event.target.value })} required />
      <textarea placeholder="Description" value={form.description} onChange={(event) => setForm({ ...form, description: event.target.value })} required />
      <input placeholder="Contact Email" value={form.contact_email} onChange={(event) => setForm({ ...form, contact_email: event.target.value })} />
      <input placeholder="Source URI" value={form.source_uri} onChange={(event) => setForm({ ...form, source_uri: event.target.value })} />
      <button type="submit">Save Use Case</button>
    </form>
  );
}
