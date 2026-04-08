from django.http import Http404
from django.shortcuts import render
from django.views import View

from modules.catalog.service_provider import get_catalog_service
from core.exceptions.domain_exceptions import CategoryNotFoundException, ProductNotFoundException


class HomeView(View):
    template_name = "catalog/home.html"

    def get(self, request):
        service = get_catalog_service()
        context = {
            "root_categories": service.get_root_categories(),
            "featured_products": service.get_featured_products(count=8),
        }
        return render(request, self.template_name, context)


class CategoryProductListView(View):
    template_name = "catalog/product_list.html"

    def get(self, request, slug):
        page = int(request.GET.get("page", 1))
        service = get_catalog_service()
        try:
            data = service.get_category_with_products(slug, page=page)
        except CategoryNotFoundException:
            raise Http404 from None
        pagination_pages = range(1, data.total_pages + 1)
        return render(
            request,
            self.template_name,
            {"data": data, "pagination_pages": pagination_pages},
        )


class ProductDetailView(View):
    template_name = "catalog/product_detail.html"

    def get(self, request, slug):
        service = get_catalog_service()
        try:
            data = service.get_product_detail(slug)
        except ProductNotFoundException:
            raise Http404 from None
        return render(
            request,
            self.template_name,
            {
                "data": data,
                "catalog_nav_active_slug": data.product.category_slug,
            },
        )


class ProductSearchView(View):
    template_name = "catalog/search_results.html"

    def get(self, request):
        query = request.GET.get("q", "").strip()
        data = None
        pagination_pages = []
        if len(query) >= 2:
            service = get_catalog_service()
            data = service.search_products(query, page=int(request.GET.get("page", 1)))
            pagination_pages = range(1, data.total_pages + 1)
        return render(
            request,
            self.template_name,
            {
                "data": data,
                "query": query,
                "pagination_pages": pagination_pages,
            },
        )
