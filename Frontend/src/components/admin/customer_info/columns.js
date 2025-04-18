import { h } from 'vue'
import DropdownAction from '@/components/admin/customer_info/DataTableDropDown.vue'
import Rating from 'primevue/rating';

export function getColumns(updateBlockedStatus) {
  return [
    {
      accessorKey: 'customer_id',
      header: () => h('div', { class: 'text-left' }, 'Customer ID'),
      cell: ({ row }) => {
        const customer_id = row.getValue('customer_id')
        return h('div', { class: 'text-left font-medium' }, customer_id)
      },
    },
    {
      accessorKey: 'user_id',
      header: () => h('div', { class: 'text-left' }, 'User ID'),
      cell: ({ row }) => {
        const user_id = row.getValue('user_id')
        return h('div', { class: 'text-left font-medium' }, user_id)
      },
    },
    {
      accessorKey: 'blocked',
      header: () => h('div', { class: 'text-left' }, 'Genuine'),
      cell: ({ row }) => {
        const blocked = row.getValue('blocked')
        return h(
          'div',
          { class: 'text-left font-medium' },
          blocked === 'NOT BLOCKED' ? '✅' : '❌'
        )
      },
    },
    {
      accessorKey: 'city',
      header: () => h('div', { class: 'text-left' }, 'City'),
      cell: ({ row }) => {
        const city = row.getValue('city')
        return h('div', { class: 'text-left font-medium' }, city)
      },
    },
    {
      accessorKey: 'state',
      header: () => h('div', { class: 'text-left' }, 'State'),
      cell: ({ row }) => {
        const state = row.getValue('state')
        return h('div', { class: 'text-left font-medium' }, state)
      },
    },
    {
      accessorKey: 'country',
      header: () => h('div', { class: 'text-left' }, 'Country'),
      cell: ({ row }) => {
        const country = row.getValue('country')
        return h('div', { class: 'text-left font-medium' }, country)
      },
    },
    {
      accessorKey: 'created_at',
      header: () => h('div', { class: 'text-left' }, 'Created At'),
      cell: ({ row }) => {
        const created_at = row.getValue('created_at')
        const formattedDate = created_at
          ? new Date(created_at).toLocaleDateString('en-GB', {
              day: '2-digit',
              month: 'long',
              year: 'numeric',
            })
          : 'N/A';
        return h('div', { class: 'text-left font-medium' }, formattedDate)
      },
    },
    {
      accessorKey: 'rating',
      header: () => h('div', { class: 'text-left' }, 'Rating'),
      cell: ({ row }) => {
        const rating = row.getValue('rating')
        return h(Rating, {
          modelValue: rating,
          readonly: true,
        })
      },
    },
    {
      id: 'actions',
      enableHiding: false,
      cell: ({ row }) => {
        const customer = row.original
        return h('div', { class: 'relative' }, h(DropdownAction, {customer, updateBlockedStatus}))
      },
    },
  ]
}
