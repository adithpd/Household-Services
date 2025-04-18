import { h } from 'vue'
import DropdownAction from '@/components/customer/booking_info/DataTableDropDown.vue'
import { format } from 'date-fns'


export function getColumns() {
  return [
    {
      accessorKey: 'booking_id',
      header: () => h('div', { class: 'text-left' }, 'Booking ID'),
      cell: ({ row }) => {
        const booking_id = row.getValue('booking_id')
        return h('div', { class: 'text-left font-medium' }, booking_id)
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
      accessorKey: 'date_time',
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
      accessorKey: 'price',
      header: () => h('div', { class: 'text-left' }, 'Price'),
      cell: ({ row }) => {
        const price = row.original.currency + " " + String(row.getValue('price'));
        return h('div', { class: 'text-left font-medium' }, price)
      },
    },
    {
      accessorKey: 'service_professional_name',
      header: () => h('div', { class: 'text-left' }, 'Service Professional Name'),
      cell: ({ row }) => {
        const service_professional_name = row.getValue('service_professional_name')
        return h('div', { class: 'text-left font-medium' }, service_professional_name)
      },
    },
    {
      id: 'actions',
      enableHiding: false,
      cell: ({ row }) => {
        return h('div', { class: 'relative' }, h(DropdownAction, {
          bookingId: row.getValue('booking_id'),
        }))
      }
    },
  ];
}
