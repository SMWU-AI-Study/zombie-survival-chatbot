interface TraitBarProps {
    label: string;
    value: number;
}

function TraitBar({ label, value }: TraitBarProps) {
    const safeValue = Math.max(0, Math.min(100, value));

    return (
        <div className="trait-bar">
            <div className="trait-info">
                <span>{label}</span>
                <strong>{safeValue}</strong>
            </div>

            <div className="trait-track">
                <div
                    className="trait-fill"
                    style={{ width: `${safeValue}%` }}
                />
            </div>
        </div>
    );
}

export default TraitBar;