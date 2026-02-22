import type { DashboardResponse } from '../types/api';

interface Props {
  data: DashboardResponse | null;
}

export function Dashboard({ data }: Props) {
  if (!data) return null;

  return (
    <section>
      <h2>Visualization Agent Dashboard</h2>
      <p>Total Use Cases: {data.total_use_cases}</p>
      <h3>By LOB</h3>
      <ul>
        {Object.entries(data.by_lob).map(([lob, count]) => (
          <li key={lob}>
            {lob}: {count}
          </li>
        ))}
      </ul>
      <h3>Recent</h3>
      <ul>
        {data.recent_use_cases.map((item) => (
          <li key={item.id}>
            {item.title} ({item.lob})
          </li>
        ))}
      </ul>
    </section>
  );
}
