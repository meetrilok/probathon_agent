import type { RequiredInputsResponse } from '../types/api';

interface Props {
  data: RequiredInputsResponse | null;
}

export function InputsChecklist({ data }: Props) {
  if (!data) return null;

  const renderGroup = (title: string, items: RequiredInputsResponse['ingestion']) => (
    <div>
      <h3>{title}</h3>
      <ul>
        {items.map((item) => (
          <li key={item.key}>
            <b>{item.label}</b> ({item.required ? 'Required' : 'Optional'}) — {item.description}
          </li>
        ))}
      </ul>
    </div>
  );

  return (
    <section>
      <h2>Required User Inputs</h2>
      {renderGroup('Ingestion', data.ingestion)}
      {renderGroup('Validation', data.validation)}
      {renderGroup('Infrastructure', data.infrastructure)}
    </section>
  );
}
