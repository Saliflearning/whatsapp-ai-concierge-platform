export function MetricCard({ value, label, note }: { value: string; label: string; note: string }) {
  return (
    <article className="metric-card">
      <strong>{value}</strong>
      <span>{label}</span>
      <small>{note}</small>
    </article>
  );
}
