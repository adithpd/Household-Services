import { h } from 'vue'
import { format } from 'date-fns'
import Rating from 'primevue/rating'

export function getColumns() {
  return [
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
      accessorKey: 'customer_name',
      header: () => h('div', { class: 'text-left' }, 'Customer Name'),
      cell: ({ row }) => {
        const customer_name = row.getValue('customer_name')
        return h('div', { class: 'text-left font-medium' }, customer_name)
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
      accessorKey: 'price_paid',
      header: () => h('div', { class: 'text-left' }, 'Price Paid'),
      cell: ({ row }) => {
        const price_paid = row.original.currency + " " + row.original.price
        return h('div', { class: 'text-left font-medium' }, price_paid)
      },
    },
    {
      accessorKey: 'customer_review',
      header: () => h('div', { class: 'text-left' }, 'Customer Review'),
      cell: ({ row }) => {
        const customer_review = row.original.customer_review
        return h('div', { class: 'text-left font-medium' }, customer_review)
      },
    },
    {
      accessorKey: 'customer_rating',
      header: () => h('div', { class: 'text-left' }, 'Customer Rating'),
      cell: ({ row }) => {
        const customer_rating = Number(row.original.customer_rating)
        return h(Rating, { modelValue: customer_rating, readonly: true, cancel: false });
      },
    },
  ];
}
