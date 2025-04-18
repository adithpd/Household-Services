import { h } from 'vue'
import DropdownAction from '@/components/admin/service_professional_verification/DataTableDropDown.vue'
import Rating from 'primevue/rating';

export function getColumns(updateVerificationStatus) {
  return [
    {
      accessorKey: 'service_professional_id',
      header: () => h('div', { class: 'text-left' }, 'SP_ID'),
      cell: ({ row }) => {
        const service_professional_id = row.getValue('service_professional_id');
        return h('div', { class: 'text-left font-medium' }, service_professional_id)
      },
    },
    {
      accessorKey: 'name',
      header: () => h('div', { class: 'text-left' }, 'Name'),
      cell: ({ row }) => {
        const name = row.getValue('name');
        return h('div', { class: 'text-left font-medium' }, name)
      },
    },
    {
      accessorKey: 'verified',
      header: () => h('div', { class: 'text-left' }, 'Verified'),
      cell: ({ row }) => {
        const verified = row.getValue('verified') === "VERIFIED";
        return h(
          'div',
          { class: 'text-left font-medium' },
          verified ? '✅' : '❌'
        )
      },
    },
    {
      accessorKey: 'email',
      header: () => h('div', { class: 'text-left' }, 'Email'),
      cell: ({ row }) => {
        const email = row.getValue('email');
        return h('div', { class: 'text-left font-medium' }, email)
      },
    },
    {
      accessorKey: 'phone',
      header: () => h('div', { class: 'text-left' }, 'Phone'),
      cell: ({ row }) => {
        const phone = row.getValue('phone');
        return h('div', { class: 'text-left font-medium' }, phone)
      },
    },
    {
      accessorKey: 'description',
      header: () => h('div', { class: 'text-left' }, 'Description'),
      cell: ({ row }) => {
        const description = row.getValue('description');
        return h('div', { class: 'text-left font-medium' }, description)
      },
    },
    {
      accessorKey: 'rating',
      header: () => h('div', { class: 'text-left' }, 'Rating'),
      cell: ({ row }) => {
        const rating = row.getValue('rating');
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
        const service_professional = row.original;
        return h('div', { class: 'relative' }, h(DropdownAction, {service_professional, updateVerificationStatus}))
      },
    },
  ]
}
