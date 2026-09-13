import type { ReactElement } from "react";

import type { TaskFieldsFragment } from "../../../fragments/TaskFields.generated";
import { cn } from "../../../utils/cn";
import { formatShortDate } from "../utils/formatDate";
import * as Styles from "./styles";

interface RecordTableProps {
  records: TaskFieldsFragment[];
  onOpenRecord: (id: string) => void;
}

const RecordTable = (props: RecordTableProps): ReactElement => {
  const { records, onOpenRecord } = props;

  return (
    <div className={Styles.cardStyles}>
      <table className={Styles.tableStyles}>
        <thead>
          <tr className={Styles.theadRowStyles}>
            <th className={Styles.thStyles} style={{ width: 112 }}>
              Type
            </th>
            <th className={Styles.thStyles}>Title</th>
            <th className={Styles.thStyles} style={{ width: 180 }}>
              Date
            </th>
            <th className={Styles.thStyles} style={{ width: 150 }}>
              Status
            </th>
          </tr>
        </thead>
        <tbody>
          {records.map((record) => {
            const isDone = record.status === "done";
            return (
              <tr
                key={record.id}
                className={Styles.rowStyles}
                onClick={() => onOpenRecord(record.id)}
              >
                <td className={Styles.tdStyles}>
                  <span className={Styles.typeTagStyles}>
                    <span className={Styles.typeDotStyles} />
                    Task
                  </span>
                </td>
                <td
                  className={cn(
                    Styles.tdStyles,
                    isDone ? Styles.titleDoneCellStyles : Styles.titleCellStyles,
                  )}
                >
                  {record.title}
                </td>
                <td className={cn(Styles.tdStyles, Styles.dateCellStyles)}>
                  {formatShortDate(record.dueAt)}
                </td>
                <td className={Styles.tdStyles}>
                  <span
                    className={cn(
                      Styles.pillBaseStyles,
                      isDone ? Styles.pillDoneStyles : Styles.pillPendingStyles,
                    )}
                  >
                    {isDone ? "Done" : "Pending"}
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
      <div className={Styles.cardFootStyles}>
        <span>
          {records.length} {records.length === 1 ? "record" : "records"}
        </span>
        <span>Every record here was created by a command</span>
      </div>
    </div>
  );
};

export default RecordTable;
