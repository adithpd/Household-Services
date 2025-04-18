import { h } from 'vue'
import DropdownAction from '@/components/admin/service_info/DataTableDropDown.vue'

export function getColumns(updateService, deleteService) {
  return [
    {
      accessorKey: 'service_id',
      header: () => h('div', { class: 'text-left' }, 'Service ID'),
      cell: ({ row }) => {
        const service_id = row.getValue('service_id')
        return h('div', { class: 'text-left font-medium' }, service_id)
      },
    },
    {
      accessorKey: 'description',
      header: () => h('div', { class: 'text-left' }, 'Description'),
      cell: ({ row }) => {
        const description = row.getValue('description')
        return h('div', { class: 'text-left font-medium' }, description)
      },
    },
    {
      accessorKey: 'currency',
      header: () => h('div', { class: 'text-left' }, 'Currency'),
      cell: ({ row }) => {
        const currency = row.getValue('currency')
        return h('div', { class: 'text-left font-medium' }, currency)
      },
    },
    {
      accessorKey: 'base_price',
      header: () => h('div', { class: 'text-left' }, 'Base Price'),
      cell: ({ row }) => {
        const base_price = row.getValue('base_price')
        return h('div', { class: 'text-left font-medium' }, base_price)
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
      id: 'actions',
      enableHiding: false,
      cell: ({ row }) => {
        const service = row.original
        return h('div', { class: 'relative' }, h(DropdownAction, {service, updateService, deleteService}))
      },
    },
  ]
}
