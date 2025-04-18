import { h } from 'vue'
import DropdownAction from '@/components/customer/request_info/ongoing_request/DataTableDropDown.vue'
import { format } from 'date-fns'


export function getColumns(handleCancelRequest) {
  return [
    {
      accessorKey: 'request_id',
      header: () => h('div', { class: 'text-left' }, 'Request ID'),
      cell: ({ row }) => {
        const request_id = row.getValue('request_id')
        return h('div', { class: 'text-left font-medium' }, request_id)
      },
    },
    {
      accessorKey: 'service_name',
      header: () => h('div', { class: 'text-left' }, 'Service Name'),
      cell: ({ row }) => {
        const service_name = row.original.keywords
        return h('div', { class: 'text-left font-medium' }, service_name)
      },
    },
    {
      accessorKey: 'start_time',
      header: () => h('div', { class: 'text-left' }, 'Date of Visit'),
      cell: ({ row }) => {
        const startDate = new Date(row.original.start_time);
        const endDate = new Date(row.original.end_time);

        const formattedDate = format(startDate, "dd MMM yyyy");
        const formattedStartTime = format(startDate, "hh:mm a");
        const formattedEndTime = format(endDate, "hh:mm a");
        return h('div', { class: 'flex flex-row gap-1' }, [
          h('span', { class: 'text-xs font-semibold bg-gray-800 text-white px-3 py-1 rounded-full inline-block' }, formattedDate),
          h('span', { class: 'text-xs font-semibold bg-blue-900 text-white px-3 py-1 rounded-full inline-block' }, `${formattedStartTime} - ${formattedEndTime}`)
        ]);
      },
    },
    {
      accessorKey: 'quote_price',
      header: () => h('div', { class: 'text-left' }, 'Quote Price'),
      cell: ({ row }) => {
        const quote_price = row.original.currency + " " + String(row.getValue('quote_price'));
        return h('div', { class: 'text-left font-medium' }, quote_price)
      },
    },
    {
      id: 'actions',
      enableHiding: false,
      cell: ({ row }) => {
        return h('div', { class: 'relative' }, h(DropdownAction, {
          requestId: row.getValue('request_id'),
          onCancel: handleCancelRequest
        }))
      }
    },
  ];
}
